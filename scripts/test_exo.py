#!/usr/bin/env python3
"""Filet de sécurité pour les 3 fixes de exo.py (§5 de l'audit).

Construit un mini-coffre en tmp et vérifie : exclusion démo/archive, liens à
alias, recherche sans accent, désambiguïsation. Sans framework.

    python3 scripts/test_exo.py   → OK si tout passe, AssertionError sinon.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exo  # noqa: E402  (import après ajustement du sys.path)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)


def build_vault(root):
    write(f"{root}/Clients/Mélanie Gross.md", "---\ntype: client\n---\n# Mélanie Gross\n")
    write(f"{root}/Clients/Chloé Simart.md", "---\ntype: client\n---\n# Chloé Simart\n")
    write(f"{root}/Devis/Chiffrage — Chloé Simart (interne).md",
          "---\ntype: chiffrage\n---\n# Chiffrage — Chloé Simart (interne)\n")
    write(f"{root}/Personnalité/Qui suis-je.md", "---\ntype: personne\n---\n# Qui suis-je\n")
    # note de projet qui cite le hub via alias — le lien entrant doit être vu
    write(f"{root}/Projets/Refonte X.md",
          "---\ntype: note-projet\n---\n# Refonte X\n\nPar [[Qui suis-je|Nathan]].\n")
    # coffre démo : ne doit JAMAIS remonter
    write(f"{root}/_to_delete/Exocortex Démo/Démo Client.md",
          "---\ntype: client\n---\n# Démo Client\n")
    # prospect archivé : exclu par défaut, visible avec include_archive
    write(f"{root}/Prospects/Archive/Vieux Prospect.md",
          "---\ntype: prospect\nstatut: À oublier\n---\n# Vieux Prospect\n")
    write(f"{root}/Prospects/Coiffure Océane.md",
          "---\ntype: prospect\nstatut: À contacter\n---\n# Coiffure Océane\n")


def run():
    with tempfile.TemporaryDirectory() as root:
        build_vault(root)
        notes = exo.load_notes(root)
        names = {n["name"] for n in notes}

        # a) exclusion démo + archive
        assert "Démo Client" not in names, "le coffre démo (_to_delete/) remonte encore"
        assert "Vieux Prospect" not in names, "l'archive prospect remonte par défaut"
        assert "Coiffure Océane" in names, "un prospect normal a disparu"
        with_archive = {n["name"] for n in exo.load_notes(root, include_archive=True)}
        assert "Vieux Prospect" in with_archive, "--include-archive ne réintègre pas l'archive"
        assert "Démo Client" not in with_archive, "le démo doit rester exclu même avec archive"

        # b) lien entrant à alias [[Qui suis-je|Nathan]]
        hub = next(n for n in notes if n["name"] == "Qui suis-je")
        assert "Refonte X" in exo.incoming_links(notes, hub), "lien entrant à alias invisible"

        # c) recherche sans accent
        best, _ = exo.best_matches(notes, "Melanie")
        assert best is not None and best["name"] == "Mélanie Gross", "accent-insensibilité KO"

        # c) désambiguïsation Chloé (cliente vs chiffrage)
        _, tied = exo.best_matches(notes, "Chloé")
        tied_names = {n["name"] for n in tied}
        assert {"Chloé Simart", "Chiffrage — Chloé Simart (interne)"} <= tied_names, \
            f"ambiguïté Chloé non détectée : {tied_names}"

    print("OK — 3 fixes exo.py vérifiés")


if __name__ == "__main__":
    run()
