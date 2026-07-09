#!/usr/bin/env python3
"""exo.py — navigation rapide dans le coffre Obsidian Exocortex.

Sans dépendance externe. Parse le frontmatter YAML (champs scalaires et listes
simples) de chaque note .md et offre quelques sous-commandes de recherche.

Usage :
    python3 exo.py index               [--vault PATH] [--type TYPE]
    python3 exo.py find  <requête>     [--vault PATH]
    python3 exo.py get   <nom>         [--vault PATH]
    python3 exo.py field <clé>         [--vault PATH] [--value V]
    python3 exo.py links <nom>         [--vault PATH]

Le coffre est auto-détecté (dossier contenant .obsidian) si --vault est omis ;
on peut aussi fixer la variable d'environnement EXOCORTEX_VAULT.
"""
import argparse
import os
import re
import sys
from difflib import SequenceMatcher


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


def load_notes(vault):
    notes = []
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
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
    q = query.lower()
    best = 0.0
    for cand in (note["name"], note["title"]):
        c = cand.lower()
        if q == c:
            return 1.0
        if q in c:
            best = max(best, 0.9)
        best = max(best, SequenceMatcher(None, q, c).ratio())
    return best


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
    ranked = sorted(notes, key=lambda n: score(args.name, n), reverse=True)
    if not ranked or score(args.name, ranked[0]) < 0.3:
        print(f"Aucune fiche ne correspond à « {args.name} ».")
        return
    n = ranked[0]
    print(f"# Fiche : {n['rel']}\n")
    print(n["text"].rstrip())


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
    ranked = sorted(notes, key=lambda n: score(args.name, n), reverse=True)
    if not ranked or score(args.name, ranked[0]) < 0.3:
        print(f"Aucune fiche ne correspond à « {args.name} ».")
        return
    n = ranked[0]
    out = set(re.findall(r"\[\[([^\]]+)\]\]", n["text"]))
    print(f"Liens sortants de « {n['name']} » : "
          + (", ".join(sorted(out)) if out else "aucun"))
    incoming = [m["name"] for m in notes
                if m is not n and re.search(r"\[\[" + re.escape(n["name"]) + r"\]\]", m["text"])]
    print(f"Liens entrants (qui citent « {n['name']} ») : "
          + (", ".join(sorted(incoming)) if incoming else "aucun"))


def main():
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--vault", help="Chemin du coffre (sinon auto-détecté)")
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
    notes = load_notes(vault)
    if not notes:
        print(f"Aucune note .md trouvée dans {vault}.", file=sys.stderr)
        sys.exit(1)

    {"index": cmd_index, "find": cmd_find, "get": cmd_get,
     "field": cmd_field, "links": cmd_links}[args.cmd](notes, args)


if __name__ == "__main__":
    main()
