# Conventions du coffre Exocortex

Référence pour lire et surtout **écrire** des fiches sans casser l'existant.
Observée sur le coffre de l'utilisateur ; à compléter si de nouveaux dossiers/champs
apparaissent.

## Arborescence

```
Exocortex/
├── Clients/        → une fiche par personne physique (interlocuteur)      type: client
├── Entreprises/    → une fiche par personne morale (société du client)    type: entreprise
├── Prospects/      → une fiche par entreprise à démarcher                 type: prospect
│   └── Archive/    → prospects « À oublier » (exclus des recherches exo.py)
├── Personnalité/   → notes sur l'utilisateur lui-même (hub + sous-fiches)        type: personne / référentiel
├── Clients.md      → index (MOC) des clients, groupé par statut           type: index
└── Prospects.md    → index (MOC) des prospects : Pipeline + secteurs + Archive   type: index
```

D'autres dossiers viendront (Projets, Devis, Réunions, Factures…). Quand un nouveau
type apparaît, déduis son schéma en lisant 1-2 fiches existantes du dossier avant
d'écrire.

Les fichiers `*.md` à la racine portant `type: index` sont des **cartes (MOC)** : des
vues d'ensemble en wikilinks. Quand tu crées/convertis/supprimes une fiche, pense à
mettre à jour l'index correspondant (Clients.md, Prospects.md) pour qu'elle reste reliée.

## Fiche CLIENT (`Clients/Prénom NOM.md`)

Frontmatter type observé :

```yaml
---
type: client
statut: Client actif          # Client actif / Client inactif (les prospects ont leur propre dossier)
email: prenom@exemple.com
téléphone: "+33 6 12 34 56 78" # guillemets requis si commence par +
site_web: https://…
date_début: 2026-05-12         # AAAA-MM-JJ
budget:                        # vide si inconnu — on garde la clé
projet: Description courte du projet
avis_google: false             # booléen
entreprises:
  - "[[Nom Entreprise]]"       # wikilink vers Entreprises/Nom Entreprise.md
source_notion: https://app.notion.com/p/…
---

# Prénom NOM

- **Né en** : …            # infos d'identité optionnelles
- **Rôle** : Président de [[Nom Entreprise]] (depuis …)
- **Source** : …

## Suivi projet

- Puces chronologiques du suivi (devis, paiements, RDV, démos…).
```

## Fiche ENTREPRISE (`Entreprises/Nom.md`)

```yaml
---
type: entreprise
adresse: "12 rue …, 75000 Ville"   # guillemets (contient des virgules)
téléphone:
email_facturation: contact@…
siret_siren: "940 852 932"
site_web: exemple.fr
clients:
  - "[[Prénom NOM]]"               # wikilink vers Clients/Prénom NOM.md
source_notion: https://app.notion.com/p/…
---

# Nom Entreprise

## Informations légales

- **Forme juridique** : …
- **SIREN** / **SIRET siège** / **TVA intracommunautaire** : …
- **Capital social**, **Date de création**, **Activité (NAF)**, **Adresse** : …

## Dirigeant

- [[Prénom NOM]] — Rôle (depuis …)
```

## Fiche PROSPECT (`Prospects/Nom Entreprise.md`)

Une entreprise à démarcher (pas encore cliente). Nommée par son nom commercial.

```yaml
---
type: prospect
statut: À contacter        # cycle Loom : À contacter → À produire → Contenu envoyé → Devis à envoyer → Devis envoyé → Signé | À oublier
secteur: "PME – Services"  # BTP / PME – Commerce / PME – Services
contact:                   # interlocuteur si connu
email:
téléphone: "03 81 39 00 85"
site_actuel: https://…     # site existant, souvent à refondre
lien_loom:                 # vidéo Loom de prospection
lien_prototype:            # prototype Claude (livrable de prospection, à côté du Loom)
source_notion: https://app.notion.com/p/…
---

# Nom Entreprise

## Notes

Analyse de la cible : activité, localisation, état du site actuel, angle d'approche.
```

À la création, ajouter une ligne dans l'index `Prospects.md` sous le bon secteur :
`- [[Nom Entreprise]] · Activité, Ville (dpt)`. Conversion en client : voir le skill
exocortex-prospects (crée entreprise + client, met à jour les deux index).

## Fiche PERSONNALITÉ (`Personnalité/…`)

Notes sur l'utilisateur lui-même. `Qui suis-je.md` (`type: personne`) est le **hub** : coordonnées
en frontmatter, activité/méthode dans le corps, et une section « Sous-fiches me concernant »
qui relie en wikilinks les autres notes perso. Les documents de référence (ex.
`Style rédactionnel.md`) portent `type: référentiel`. Toute nouvelle fiche perso se
range dans `Personnalité/` puis s'ajoute en wikilink au hub.

## Règles d'or pour l'écriture

1. **Le nom de fichier = le titre H1**, sans extension. C'est ce que ciblent les
   wikilinks `[[…]]`. Ne renomme pas l'un sans l'autre. Pour la **casse** d'un nom de
   personne, reprends l'orthographe telle que l'utilisateur l'a fournie (le coffre mélange
   « Fabian GAMMA » et « Catherine Gouy » — il n'y a pas de règle stricte ; ne force
   pas le nom de famille en majuscules).
2. **Conserve toutes les clés du frontmatter**, même vides. L'homogénéité permet les
   requêtes par champ ; supprimer une clé crée des trous silencieux.
3. **Liens bidirectionnels obligatoires.** Client ↔ Entreprise doivent se pointer
   mutuellement (`entreprises:` côté client, `clients:` côté entreprise). Si la cible
   d'un lien n'existe pas, crée la fiche correspondante (au moins en brouillon avec son
   frontmatter type).
4. **Édition chirurgicale.** Pour changer une valeur, modifie la seule ligne concernée
   du frontmatter ; ne réécris jamais le corps « Suivi projet » sauf demande explicite —
   c'est l'historique du dossier.
5. **Formats.** Dates `AAAA-MM-JJ`. Téléphones et adresses entre guillemets s'ils
   contiennent `+`, `,` ou `:`. Booléens en minuscules (`true`/`false`).
6. **Source.** Quand l'info vient de Notion, garde/renseigne `source_notion`. Quand elle
   vient d'ailleurs (societe.com, Gmail…), cite-la dans le corps comme dans l'existant.
   Pour une fiche saisie directement par l'utilisateur (sans import), laisse `source_notion` vide.
7. **Index à jour.** Toute création/conversion/suppression de fiche doit se refléter dans
   l'index MOC concerné (Clients.md, Prospects.md) ; sinon la fiche devient orpheline dans
   la vue graphique.
8. **Pas de date inventée.** `date_début` (signature/démarrage d'un client) reste vide tant
   qu'il n'a pas signé ; ne devine jamais une date.
