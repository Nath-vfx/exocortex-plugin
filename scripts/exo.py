#!/usr/bin/env python3
"""exo.py — navigation rapide dans le coffre Obsidian Exocortex.

Sans dépendance externe. Parse le frontmatter YAML (champs scalaires et listes
simples) de chaque note .md et offre quelques sous-commandes de recherche.

Usage :
    python3 exo.py index               [--vault PATH] [--type TYPE] [--include-archive]
    python3 exo.py find  <requête>     [--vault PATH] [--include-archive]
    python3 exo.py get   <nom>         [--vault PATH] [--include-archive]
    python3 exo.py field <clé>         [--vault PATH] [--value V] [--include-archive]
    python3 exo.py links <nom>         [--vault PATH] [--include-archive]

Le coffre est auto-détecté (dossier contenant .obsidian) si --vault est omis ;
on peut aussi fixer la variable d'environnement EXOCORTEX_VAULT.

`_to_delete/` (coffre démo) et `Prospects/Archive/` (prospects « À oublier ») sont
exclus par défaut ; `--include-archive` réintègre l'archive.
"""
import argparse
import os
import re
import sys
import unicodedata
from difflib import SequenceMatcher

# Dossiers jamais indexés : coffre démo et dépendances. Le .gitignore du coffre
# exclut déjà _to_delete/, mais exo.py, lui, l'avalait.
IGNORED_DIRS = {"_to_delete", "node_modules"}
# Dossier d'archive prospect, exclu sauf --include-archive (relatif au coffre).
ARCHIVE_REL = os.path.join("Prospects", "Archive")


def find_vault(explicit=None):
    candidates = []
    if explicit:
        candidates.append(explicit)
    if os.environ.get("EXOCORTEX_VAULT"):
        candidates.append(os.environ["EXOCORTEX_VAULT"])
    for c in candidates:
        if c and os.path.isdir(os.path.join(c, ".obsidian")):
            return c
        if c and os.path.isdir(c):
            return c  # accepte un dossier même sans .obsidian
    # Auto-détection : remonte depuis le cwd, puis balaie les dossiers montés.
    here = os.getcwd()
    while here and here != "/":
        if os.path.isdir(os.path.join(here, ".obsidian")):
            return here
        here = os.path.dirname(here)
    for base in ("/sessions",):
        for root, dirs, _ in os.walk(base):
            if ".obsidian" in dirs:
                return root
            # ne pas descendre trop profond
            if root.count(os.sep) - base.count(os.sep) > 4:
                dirs[:] = []
    return None


def norm(s):
    """Minuscule sans accents (NFD + suppression des marques combinantes)."""
    return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                   if unicodedata.category(c) != "Mn")


def split_frontmatter(text):
    """Renvoie (dict_frontmatter, corps)."""
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    raw, body = m.group(1), m.group(2)
    fm = {}
    current_key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        # élément de liste appartenant à la clé précédente
        m_item = re.match(r"^\s+-\s+(.*)$", line)
        if m_item and current_key is not None:
            val = m_item.group(1).strip().strip('"').strip("'")
            fm.setdefault(current_key, [])
            if isinstance(fm[current_key], list):
                fm[current_key].append(val)
            continue
        m_kv = re.match(r"^([^:\s][^:]*):\s?(.*)$", line)
        if m_kv:
            key = m_kv.group(1).strip()
            val = m_kv.group(2).strip()
            current_key = key
            if val == "":
                fm[key] = ""  # valeur vide ou début de liste
            else:
                fm[key] = val.strip('"').strip("'")
    return fm, body


def load_notes(vault, include_archive=False):
    notes = []
    for root, dirs, files in os.walk(vault):
        rel_root = os.path.relpath(root, vault)
        kept = []
        for d in dirs:
            if d.startswith(".") or d in IGNORED_DIRS:
                continue
            rel = os.path.normpath(os.path.join(rel_root, d))
            if not include_archive and rel == ARCHIVE_REL:
                continue
            kept.append(d)
        dirs[:] = kept
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                try:
                    text = open(path, encoding="utf-8").read()
                except Exception:
                    continue
                fm, body = split_frontmatter(text)
                title = None
                m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
                if m:
                    title = m.group(1).strip()
                notes.append({
                    "path": path,
                    "rel": os.path.relpath(path, vault),
                    "name": os.path.splitext(f)[0],
                    "title": title or os.path.splitext(f)[0],
                    "fm": fm,
                    "body": body,
                    "text": text,
                })
    return notes


def score(query, note):
    q = norm(query)
    best = 0.0
    for cand in (note["name"], note["title"]):
        c = norm(cand)
        if q == c:
            return 1.0
        if q in c:
            best = max(best, 0.9)
        best = max(best, SequenceMatcher(None, q, c).ratio())
    return best


def best_matches(notes, name, threshold=0.3, ambiguity=0.1):
    """Renvoie (meilleure_note|None, candidats_ex_aequo).

    `candidats_ex_aequo` = toutes les notes dont le score est à moins de
    `ambiguity` du meilleur (et au-dessus du seuil) — sert à afficher une liste
    plutôt que de trancher en silence entre deux fiches proches.
    """
    ranked = sorted(notes, key=lambda n: score(name, n), reverse=True)
    if not ranked or score(name, ranked[0]) < threshold:
        return None, []
    top = score(name, ranked[0])
    tied = [n for n in ranked
            if score(name, n) >= threshold and top - score(name, n) < ambiguity]
    return ranked[0], tied


def incoming_links(notes, target):
    """Notes qui citent `target`, y compris via alias `[[Nom|x]]` ou ancre `[[Nom#s]]`."""
    pat = re.compile(r"\[\[" + re.escape(target["name"]) + r"\s*(\||#|\]\])")
    return [m["name"] for m in notes if m is not target and pat.search(m["text"])]


def outgoing_links(note):
    """Cibles des wikilinks sortants, alias/ancre retirés."""
    return {re.split(r"[|#]", raw, 1)[0].strip()
            for raw in re.findall(r"\[\[([^\]]+)\]\]", note["text"])}


def _print_ambiguous(name, tied):
    print(f"Plusieurs fiches correspondent à « {name} » :")
    for n in tied:
        print(f"  {n['name']:<28} {n['rel']}")
    print("Précise le nom exact pour lever l'ambiguïté.")


def cmd_index(notes, args):
    by_type = {}
    for n in notes:
        t = n["fm"].get("type", "(sans type)")
        by_type.setdefault(t, []).append(n)
    for t in sorted(by_type):
        if args.type and t != args.type:
            continue
        print(f"== {t} ({len(by_type[t])}) ==")
        for n in sorted(by_type[t], key=lambda x: x["name"]):
            print(f"  {n['name']:<28} {n['rel']}")


def cmd_find(notes, args):
    ranked = sorted(notes, key=lambda n: score(args.query, n), reverse=True)
    for n in ranked[:8]:
        s = score(args.query, n)
        if s < 0.3:
            break
        print(f"{s:.2f}  {n['name']:<28} {n['rel']}")


def cmd_get(notes, args):
    best, tied = best_matches(notes, args.name)
    if best is None:
        print(f"Aucune fiche ne correspond à « {args.name} ».")
        return
    if len(tied) > 1:
        _print_ambiguous(args.name, tied)
        return
    print(f"# Fiche : {best['rel']}\n")
    print(best["text"].rstrip())


def cmd_field(notes, args):
    hits = []
    for n in notes:
        if args.key in n["fm"]:
            val = n["fm"][args.key]
            if args.value:
                joined = " ".join(val) if isinstance(val, list) else str(val)
                if args.value.lower() not in joined.lower():
                    continue
            hits.append((n, val))
    if not hits:
        print(f"Aucune fiche avec le champ « {args.key} »"
              + (f" = « {args.value} »" if args.value else "") + ".")
        return
    for n, val in hits:
        shown = ", ".join(val) if isinstance(val, list) else (val or "(vide)")
        print(f"{n['name']:<28} {args.key}: {shown}")


def cmd_links(notes, args):
    best, tied = best_matches(notes, args.name)
    if best is None:
        print(f"Aucune fiche ne correspond à « {args.name} ».")
        return
    if len(tied) > 1:
        _print_ambiguous(args.name, tied)
        return
    out = outgoing_links(best)
    print(f"Liens sortants de « {best['name']} » : "
          + (", ".join(sorted(out)) if out else "aucun"))
    incoming = incoming_links(notes, best)
    print(f"Liens entrants (qui citent « {best['name']} ») : "
          + (", ".join(sorted(incoming)) if incoming else "aucun"))


def main():
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--vault", help="Chemin du coffre (sinon auto-détecté)")
    parent.add_argument("--include-archive", action="store_true",
                        help="Inclure Prospects/Archive/ (exclu par défaut)")
    p = argparse.ArgumentParser(description="Navigation dans le coffre Exocortex",
                                parents=[parent])
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("index", parents=[parent]); sp.add_argument("--type")
    sp = sub.add_parser("find", parents=[parent]); sp.add_argument("query")
    sp = sub.add_parser("get", parents=[parent]); sp.add_argument("name")
    sp = sub.add_parser("field", parents=[parent]); sp.add_argument("key"); sp.add_argument("--value")
    sp = sub.add_parser("links", parents=[parent]); sp.add_argument("name")
    args = p.parse_args()

    vault = find_vault(args.vault)
    if not vault:
        print("Coffre introuvable. Précise --vault ou EXOCORTEX_VAULT.", file=sys.stderr)
        sys.exit(2)
    notes = load_notes(vault, args.include_archive)
    if not notes:
        print(f"Aucune note .md trouvée dans {vault}.", file=sys.stderr)
        sys.exit(1)

    {"index": cmd_index, "find": cmd_find, "get": cmd_get,
     "field": cmd_field, "links": cmd_links}[args.cmd](notes, args)


if __name__ == "__main__":
    main()
