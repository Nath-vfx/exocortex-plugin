---
name: exocortex-projets
description: >
  Parcourt et gère les PROJETS du coffre Obsidian Exocortex de l'utilisateur : le dossier
  Projets/ (une note hub par projet, type "projet") plus l'index Projets.md. Un projet porte
  le statut (ex. "En cours"), le client et l'entreprise (wikilinks), la date de début, le
  budget, les prestations, et des sous-notes détaillées (type "note-projet" : brief, business
  & SEO, contenu, design…). Utilise ce skill pour LISTER/filtrer les projets (par statut, par
  client, par entreprise), SAVOIR OÙ EN EST un projet (avancement, budget, liens maquette/site),
  CRÉER un projet (note hub + sous-notes + inscription dans l'index), et METTRE À JOUR son
  statut ou sa chronologie. Déclenche sur « mes projets », « mes projets en cours », « où en
  est le projet X », « le budget / l'avancement du projet X », « les projets du client Y / de
  l'entreprise Z », « crée un projet pour … », « passe le projet X en terminé », « les projets
  à cadrer ». Pour la fiche du CLIENT lui-même → exocortex-clients ; pour les infos légales /
  facturation de l'ENTREPRISE → exocortex-entreprises ; pour un PROSPECT pas encore signé →
  exocortex-prospects (la conversion prospect → client y est gérée).
---

# Exocortex — Projets

Le dossier `Projets/` regroupe les projets clients de l'utilisateur : **une note hub par projet**
(`type: projet`), avec statut, client, entreprise, budget et prestations, et un index `Projets.md`.
Une note hub peut être une **dossier-note** (`Projets/<Nom>/<Nom>.md` + des sous-notes détaillées
`type: note-projet` dans le même dossier) ou une **note simple** (`Projets/<Nom>.md` seule) — ne
suppose pas qu'un dossier existe. Autonome : recherche ET écriture. Localise le coffre et son mode
d'accès via `${CLAUDE_PLUGIN_ROOT}/references/acces-coffre.md`, puis utilise
`${CLAUDE_PLUGIN_ROOT}/scripts/exo.py` ; règles d'écriture dans
`${CLAUDE_PLUGIN_ROOT}/references/conventions.md`.

## Lister / filtrer les projets

```bash
EXO="${CLAUDE_PLUGIN_ROOT}/scripts/exo.py"
python3 "$EXO" field type   --vault "$VAULT" --value projet        # tous les projets
python3 "$EXO" field statut --vault "$VAULT" --value "En cours"    # par statut
python3 "$EXO" get "Refonte site QUALIROAD" --vault "$VAULT"       # une note hub (floue)
python3 "$EXO" links "Refonte site QUALIROAD" --vault "$VAULT"     # client, entreprise, sous-notes
```

Les projets **à cadrer** (pas encore démarrés) n'ont **pas** de note : ils vivent uniquement en
puces sous `## À cadrer` dans `Projets.md`. Pour la vue d'ensemble, lis toujours `Projets.md` en plus
du `field type`.

## Schéma d'une note de projet

Note hub (`type: projet`) — garde toutes les clés, laisse vides celles qu'on n'a pas encore :

```yaml
---
type: projet
statut: En cours              # statut ouvert (seul "En cours" observé aujourd'hui)
client: "[[Fabian GAMMA]]"    # wikilink vers Clients/, entre guillemets
entreprise: "[[QUALIROAD]]"   # wikilink vers Entreprises/, entre guillemets
date_début: 2026-06-06        # AAAA-MM-JJ (clé accentuée)
budget: "1 875 €"             # chaîne avec € (peut être vide)
prestations: Refonte du site web + fiche Google Business Profile
maquette:                     # URL prototype/staging (optionnel)
site_actuel:                  # site existant à refondre (optionnel)
domaine_envisage:             # nom de domaine visé (optionnel)
devis_réf:                    # réf. du devis lié, ex. DEV-2026-07-004 (optionnel)
source_notion:                # page Notion source (optionnel)
---

# Nom du projet

## En bref
- Client : [[Prénom NOM]] ([[Entreprise]])
- Prestations : …
- Budget : … · Paiement : …
- Statut : En cours

## Liens du projet
- Maquette : …
- Site actuel : …

## Notes détaillées
- [[Brief & attentes]]
- [[Business & SEO]]
- [[Contenu & arborescence]]
- [[Design & technique]]

## Chronologie
- 2026-06-06 — Lancement.
- **Prochaines étapes** : …
```

Sous-note détaillée (`type: note-projet`), dans le même dossier que le hub, avec back-ref :

```yaml
---
type: note-projet
projet: "[[Nom du projet]]"
---
```

## Ouvrir / consulter un projet

`get` la note hub, puis ses sous-notes (même dossier, ou `field projet --value "[[<Nom>]]"`). Le corps
suit toujours `## En bref` → `## Liens du projet` → `## Notes détaillées` → `## Chronologie`. Si un
champ du frontmatter est vide, l'info est souvent dans le corps ou la note détaillée — n'invente jamais
une valeur absente.

## Créer un projet

Modèle de référence : `Projets/Refonte site QUALIROAD/`. Cas riche (dossier-note) :

1. **Note hub** `Projets/<Nom>/<Nom>.md` avec le schéma ci-dessus. `client` et `entreprise` pointent
   vers des fiches existantes (sinon, crée-les d'abord via exocortex-clients / exocortex-entreprises).
2. **Sous-notes standard** dans le même dossier — `Brief & attentes`, `Business & SEO`,
   `Contenu & arborescence`, `Design & technique` (+ toute note spécifique au projet), chacune
   `type: note-projet` + `projet: "[[<Nom>]]"`, et listées dans `## Notes détaillées` du hub.
3. **Liens bidirectionnels** : la fiche client (`projet:` / suivi) et la fiche entreprise doivent
   pointer en retour vers le projet, selon `references/conventions.md`.
4. **Inscris le projet dans `Projets.md`** sous `## En cours`, au format réel
   `- [[<Nom>]] — [[Client]] / [[Entreprise]] · <prestations courtes> · <budget>`. S'il figurait sous
   `## À cadrer`, **retire-l'y** (il a désormais une note).

Cas léger : un projet minimal peut n'être qu'une **note simple** `Projets/<Nom>.md` (`type: projet`),
sans dossier ni sous-notes. **Montre toujours le plan (fichiers créés / modifiés) avant d'exécuter.**

## Mettre à jour un projet

Édition chirurgicale du frontmatter (ex. `statut: En cours` → `Terminé`) et **puces datées** ajoutées
en fin de `## Chronologie` — n'écrase pas l'historique, garde toutes les clés. Un **changement de statut
actualise la ligne** dans `Projets.md` (et, si le projet est terminé/archivé, la sort de `## En cours`).

## Index `Projets.md`

Deux étages à garder en phase avec la réalité :
- `## En cours` — un projet **par note existante** (`type: projet`).
- `## À cadrer` — projets pressentis **sans note encore** (simples puces, ex. « M-Energies Pro »,
  « Léa Kleindienst »). Quand l'un obtient sa note, il **migre** de `## À cadrer` vers `## En cours`.

## Vérification

`python3 "$EXO" get "<nom>" --vault "$VAULT"` doit renvoyer un YAML valide ;
`python3 "$EXO" links "<nom>" --vault "$VAULT"` doit montrer le client et l'entreprise (liens dans les
deux sens) et les sous-notes ; le projet doit apparaître dans `Projets.md` sous la bonne section.
