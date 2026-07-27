---
name: exocortex-clients
description: >
  Recherche et écriture des fiches CLIENTS du coffre Obsidian Exocortex de l'utilisateur
  (dossier Clients/, une note par interlocuteur). Utilise ce skill pour retrouver une
  donnée d'un client actif (téléphone, email, statut, projet, avancement, lien Notion),
  pour CRÉER une fiche client, METTRE À JOUR un champ (changer un statut, ajouter un
  téléphone, noter une étape de suivi), ou gérer le lien d'un client vers sa/ses
  entreprise(s). Déclenche sur « ajoute/crée un client », « mets à jour la fiche de
  tel client », « le tel/mail/statut de tel client », « relie tel client à telle
  société ». Pour un PROSPECT (statut Prospect) ou une conversion prospect→client,
  préfère exocortex-prospects ; pour les infos légales d'une société, exocortex-entreprises.
---

# Exocortex — Clients

Gère les fiches du dossier `Clients/` : une note Markdown par personne (l'interlocuteur),
avec un frontmatter YAML structuré et un corps « Suivi projet ». Autonome : ce skill sait
chercher ET écrire. Localise le coffre et son mode d'accès via
`${CLAUDE_PLUGIN_ROOT}/references/acces-coffre.md`, puis utilise
le script partagé `${CLAUDE_PLUGIN_ROOT}/scripts/exo.py`. Le schéma complet et les règles
d'or sont dans `${CLAUDE_PLUGIN_ROOT}/references/conventions.md` — **lis-le avant d'écrire**.

## Rechercher un client

```bash
EXO="${CLAUDE_PLUGIN_ROOT}/scripts/exo.py"
python3 "$EXO" get "Mehdi"   --vault "$VAULT"            # fiche entière (floue)
python3 "$EXO" field statut  --vault "$VAULT" --value "Client actif"
python3 "$EXO" links "Fabian GAMMA" --vault "$VAULT"     # entreprise(s) rattachée(s)
```

Champ vide dans le frontmatter → vérifie le corps « Suivi projet », l'info y est souvent.

## Schéma d'une fiche client

```yaml
---
type: client
statut: Client actif          # Prospect / Client actif / Client inactif
email:
téléphone: "+33 6 12 34 56 78" # guillemets si commence par +
site_web:
date_début: 2026-05-12         # AAAA-MM-JJ (date de signature/démarrage)
budget:
projet: Description courte
avis_google: false
entreprises:
  - "[[Nom Entreprise]]"
source_notion:
---

# Prénom NOM

- **Rôle** : … de [[Nom Entreprise]] (depuis …)

## Suivi projet

- Puces chronologiques (devis, paiements, RDV, démos…).
```

## Créer / mettre à jour — règles essentielles

1. **Nom de fichier = titre H1** (`Clients/Prénom NOM.md`). C'est la cible des wikilinks ;
   reprends l'orthographe et la casse fournies par l'utilisateur, ne force pas le nom en majuscules.
2. **Conserve toutes les clés** du frontmatter, même vides — ça garde les fiches homogènes
   et requêtables.
3. **Lien bidirectionnel obligatoire.** Si tu ajoutes `entreprises: [[X]]`, ajoute
   `clients: [[Prénom NOM]]` sur la fiche `Entreprises/X.md`. Si X n'existe pas, crée-la
   (au moins son frontmatter type) — au besoin via exocortex-entreprises.
4. **Édition chirurgicale.** Pour changer une valeur, modifie la seule ligne du frontmatter ;
   ne réécris jamais le corps « Suivi projet » (c'est l'historique), ajoute une puce.
5. **Formats.** Dates `AAAA-MM-JJ` ; booléens minuscules ; pas de date inventée.

Avant d'enregistrer, montre à l'utilisateur ce que tu vas écrire et où.

## Vérification

Après écriture : `python3 "$EXO" get "<nom>" --vault "$VAULT"` ne doit pas planter (YAML
valide) et `python3 "$EXO" links "<nom>" --vault "$VAULT"` doit montrer le lien entreprise
répondu des deux côtés.
