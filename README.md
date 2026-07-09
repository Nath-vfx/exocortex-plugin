# Exocortex (plugin)

Navigation, recherche et écriture dans le coffre Obsidian **Exocortex** de Nathan — sa
mémoire externe sur ses clients et leurs entreprises (notes Markdown à frontmatter YAML,
reliées par des wikilinks `[[…]]`).

## Installation

Distribué via la marketplace `banan-agency` (`.claude-plugin/marketplace.json`) :

```
/plugin marketplace add <repo>
/plugin install exocortex@banan-agency
```

## Architecture

Un skill **routeur généraliste** + trois **sous-skills** spécialisés et autonomes :

| Skill | Rôle |
|-------|------|
| `exocortex` | Point d'entrée. Localise le coffre, fait les recherches simples, et aiguille vers le bon sous-skill. À utiliser en cas de doute. |
| `exocortex-clients` | Recherche et écriture des fiches **Clients** (clients actifs) : coordonnées, statut, projet, liens entreprise. |
| `exocortex-entreprises` | Fiches **Entreprises** : infos légales (SIRET, TVA, forme juridique), facturation, dirigeants. |
| `exocortex-prospects` | Cycle de vie **prospect** : ajout, suivi, et conversion prospect → client. |
| `exocortex-personnalite` | Dossier **Personnalité/** : infos sur Nathan lui-même (identité, contact, méthode) et son **style rédactionnel** pour écrire des messages qui sonnent comme lui. |

## Ressources partagées

- `scripts/exo.py` — outil de navigation sans dépendance (`index`, `find`, `get`, `field`,
  `links`). Auto-détecte le coffre (dossier contenant `.obsidian`) ou via `--vault`.
- `references/conventions.md` — schéma des fiches, nommage, règles de wikilink. Référence
  commune à tous les sous-skills pour l'écriture.

## Principes

- Le coffre ne contient que les clients de Nathan et leurs entreprises ; le plugin ne se
  déclenche pas pour des infos publiques sur des tiers ni des questions générales.
- Écriture chirurgicale : on modifie le champ concerné, on n'écrase jamais l'historique de
  suivi ; les liens client ↔ entreprise restent bidirectionnels.
- Conçu pour grandir : la structure est recensée dynamiquement, prête pour de futurs
  dossiers (Projets, Devis, Réunions…).
