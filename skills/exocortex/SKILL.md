---
name: exocortex
description: >
  Point d'entrée généraliste du coffre Obsidian "Exocortex" de l'utilisateur (sa mémoire
  externe sur ses clients et leurs entreprises, en notes Markdown/YAML). Utilise ce
  skill DÈS QU'on cherche ou met à jour une info propre à l'utilisateur, à un de ses clients
  ou à la société d'un client : téléphone, email, adresse, SIRET/SIREN, TVA, statut,
  budget ou avancement d'un projet, dirigeant, lien Notion, suivi d'un dossier — ou
  pour « retrouve dans mon Exocortex / mes notes / mon coffre ». Ce skill localise le
  coffre, fait les recherches simples, et AIGUILLE vers le bon sous-skill : exocortex-
  clients, exocortex-entreprises (infos légales), exocortex-prospects (ajout/conversion),
  exocortex-projets (avancement/gestion des projets) et exocortex-personnalite (infos sur
  l'utilisateur, et écrire dans sa voix). En cas de doute,
  passe d'abord par ici. NE
  PAS utiliser pour des infos publiques sur des tiers (SIRET/adresse d'une enseigne,
  numéro d'une administration → web), des questions générales (taux de TVA, syntaxe
  YAML), ni une note Obsidian sans lien avec un client/une entreprise.
---

# Exocortex — aiguilleur

L'Exocortex est le coffre Obsidian de l'utilisateur : sa mémoire externe sur ses clients et
leurs entreprises. Ce skill est le **point d'entrée**. Son rôle : localiser le coffre,
répondre vite aux recherches simples, et **router** les demandes spécialisées vers le
sous-skill compétent. Garde-le léger ; la logique métier détaillée vit dans les
sous-skills.

## Étape 0 — localiser le coffre et son mode d'accès

Suis la cascade de `${CLAUDE_PLUGIN_ROOT}/references/acces-coffre.md` : elle donne `$VAULT`
**et** le mode d'accès (direct au shell vs pont d'appareil), qui change la façon d'écrire.
Ne code jamais un chemin en dur. Puis recense la structure (elle grandit) avant d'agir :

```bash
EXO="${CLAUDE_PLUGIN_ROOT}/scripts/exo.py"
python3 "$EXO" index --vault "$VAULT"     # cartographie : type, nom, chemin de chaque fiche
```

## Étape 1 — comprendre l'intention et router

Identifie ce que veut l'utilisateur, puis agis selon ce tableau :

| Intention | Action |
|-----------|--------|
| **Récupérer un fait simple** (un téléphone, un email, un SIRET, un statut, où en est un projet) | Réponds directement ici (voir Étape 2). Pas besoin de sous-skill. |
| **Créer / mettre à jour une fiche CLIENT** (client actif), gérer ses liens entreprise | → **exocortex-clients** |
| **Infos légales / facturation / dirigeant d'une ENTREPRISE**, créer/MAJ une fiche entreprise | → **exocortex-entreprises** |
| **Ajouter un PROSPECT, suivre un prospect, convertir prospect → client** | → **exocortex-prospects** |
| **Consulter / créer / mettre à jour un PROJET** (avancement, statut, budget, sous-notes) | → **exocortex-projets** |
| **Info sur L'UTILISATEUR lui-même** (ses coordonnées, métier, process) ou **écrire un message dans sa voix** (email, devis, relance) | → **exocortex-personnalite** |

Router = invoquer/suivre le sous-skill correspondant (il porte le schéma détaillé et les
règles d'écriture de son domaine). En cas de chevauchement (ex. une demande touche client
ET entreprise), commence par le domaine principal de la demande ; le sous-skill gère les
liens croisés.

## Étape 2 — recherche simple (sans sous-skill)

Pour une simple lecture, préfère toujours le ciblage à la lecture exhaustive.

```bash
python3 "$EXO" get "Fabian"      --vault "$VAULT"   # fiche entière, correspondance floue
python3 "$EXO" field téléphone   --vault "$VAULT"   # toutes les fiches ayant ce champ
python3 "$EXO" links "Catherine Gouy" --vault "$VAULT"  # liens entrants/sortants
rg -i "cgouy5960@gmail.com" "$VAULT" -l               # plein texte : quelle fiche
```

Si la valeur d'un champ est vide dans le frontmatter, regarde le **corps** de la note :
l'info y figure souvent. N'invente jamais une valeur absente — dis qu'elle n'est pas
renseignée et propose de la chercher ailleurs (web, lien `source_notion`) ou de l'ajouter
(en passant alors par le sous-skill adéquat).

## Étape 3 — restituer

Réponds exactement à la question, avec la valeur et la fiche source. Sois concis : un
numéro demandé → le numéro + la fiche d'où il vient.

## Frontières (ne pas déclencher)

Ce coffre ne contient QUE les clients de l'utilisateur et leurs entreprises. N'utilise pas
l'Exocortex pour des informations publiques sur des tiers (le SIRET d'une grande enseigne,
l'adresse d'un siège connu, le numéro d'une administration → recherche web), pour des
questions de règles générales (quel taux de TVA s'applique, comment écrire un frontmatter),
ni pour des notes Obsidian sans rapport avec un client ou une entreprise.

## Référence partagée

Le schéma des fiches, le nommage et les règles de wikilink sont dans
`${CLAUDE_PLUGIN_ROOT}/references/conventions.md`. Les sous-skills s'y réfèrent pour
l'écriture ; consulte-le si tu dois écrire depuis ce skill plutôt que router.
