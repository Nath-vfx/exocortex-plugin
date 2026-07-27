---
name: exocortex-prospects
description: >
  Gère le pipeline de PROSPECTION du coffre Obsidian Exocortex de l'utilisateur : le dossier
  Prospects/ (une fiche par entreprise à démarcher, type "prospect") plus l'index
  Prospects.md. Chaque fiche porte le secteur, le statut (ex. "À contacter"), le contact,
  email, téléphone, le site actuel, un lien Loom, un lien prototype et des notes d'analyse. Utilise ce skill
  pour LISTER/filtrer les prospects (par secteur ou statut), RETROUVER une info d'un
  prospect (téléphone, site actuel, lien Loom, notes), AJOUTER un prospect, METTRE À JOUR
  son statut/ses notes, et surtout le CONVERTIR en client quand il signe (créer sa fiche
  entreprise + sa fiche client, mettre à jour les index). Déclenche sur « ajoute un
  prospect », « mes prospects à contacter », « les prospects du secteur X », « le tel/site
  de tel prospect », « tel prospect a signé / convertis-le en client ». Pour un client déjà
  actif → exocortex-clients ; pour les infos légales d'une société → exocortex-entreprises.
---

# Exocortex — Prospects

Le dossier `Prospects/` est le pipeline de prospection : **une fiche par
entreprise à démarcher** (refonte / création de site), regroupées par secteur dans l'index
`Prospects.md`. Une fiche prospect décrit une cible, pas encore un client. Autonome :
recherche ET écriture. Localise le coffre et son mode d'accès via
`${CLAUDE_PLUGIN_ROOT}/references/acces-coffre.md`, puis
utilise `${CLAUDE_PLUGIN_ROOT}/scripts/exo.py` ; règles d'écriture dans
`${CLAUDE_PLUGIN_ROOT}/references/conventions.md`.

## Lister / filtrer les prospects

```bash
EXO="${CLAUDE_PLUGIN_ROOT}/scripts/exo.py"
python3 "$EXO" field statut  --vault "$VAULT" --value "À contacter"
python3 "$EXO" field secteur --vault "$VAULT" --value "Services"
python3 "$EXO" get "Coiffure Océane" --vault "$VAULT"     # fiche entière (floue)
```

L'index `Prospects.md` a **deux étages** : `## Pipeline — ce qui bouge` (sous-sections par
étape — `À produire`, `Contenu envoyé`, `Devis à envoyer`, `Devis envoyé` — avec montant,
date et date de relance) puis `## À contacter, par secteur` (BTP / PME – Commerce /
PME – Services) puis `## Archive`. Un **compteur en tête** (« N prospects actifs — X engagés,
Y à contacter ») résume l'ensemble. Le bon étage dépend donc du **statut**, pas seulement du
secteur.

## Schéma d'une fiche prospect

```yaml
---
type: prospect
statut: À contacter        # cycle Loom : À contacter → À produire → Contenu envoyé → Devis à envoyer → Devis envoyé → Signé | À oublier
secteur: "PME – Services"  # BTP / PME – Commerce / PME – Services
contact:                   # nom de l'interlocuteur si connu
email:
téléphone: "03 81 39 00 85"
site_actuel: https://…     # site existant (souvent à refondre)
lien_loom:                 # vidéo Loom de prospection
lien_prototype:            # prototype Claude (livrable de prospection, à côté du Loom)
source_notion: https://app.notion.com/p/…
---

# Nom Entreprise

## Notes

Analyse de la cible : activité, localisation, état du site actuel, angle d'approche.
```

## Ajouter un prospect

Crée `Prospects/Nom Entreprise.md` avec le schéma ci-dessus (renseigne ce qu'on a, garde les
clés vides sinon), puis **inscris-le dans `Prospects.md` selon son statut** : un `À contacter`
va sous `## À contacter, par secteur` (bon secteur), format
`- [[Nom Entreprise]] · Activité, Ville (dpt)` ; un prospect déjà engagé (`À produire` et au-delà)
va dans `## Pipeline — ce qui bouge`, sous la sous-section de son étape, avec montant / date /
date de relance. **Recalcule ensuite le compteur d'en-tête.** Sans ligne d'index, le prospect
reste hors de la vue d'ensemble.

## Mettre à jour un prospect

Édition chirurgicale du frontmatter (ex. `statut: À contacter` → `À produire` → `Contenu envoyé`),
et puces datées dans `## Notes` pour l'historique d'approche. N'écrase pas les notes existantes.
Un **changement de statut déplace la ligne** dans `Prospects.md` (de « À contacter » vers le
Pipeline, ou d'une étape du Pipeline à la suivante) et impose de **recalculer le compteur**.

## Convertir un prospect → client (quand il signe)

Le prospect (entreprise) devient un client. Reproduis le modèle Clients/ + Entreprises/ :

1. **Crée la fiche entreprise** `Entreprises/Nom Entreprise.md` (via exocortex-entreprises) à
   partir des infos prospect + données légales (SIRET, etc. — à compléter depuis societe.com).
2. **Crée la fiche client** `Clients/Prénom NOM.md` pour l'interlocuteur (le `contact`), via
   exocortex-clients : `statut: Client actif`, `date_début` = date de signature, `projet`,
   et `entreprises: [[Nom Entreprise]]`.
3. **Lien bidirectionnel** client ↔ entreprise (`clients: [[Prénom NOM]]` en retour).
4. **Mets à jour les index** : retire la ligne du prospect dans `Prospects.md` (**et recalcule
   le compteur**), et ajoute le client sous « Clients actifs » dans `Clients.md` au format réel
   `- [[Client]] — [[Entreprise]] · Projet → [[Note de projet]]` (le lien vers la note de projet
   est un 3ᵉ champ implicite ; laisse-le tomber tant que le projet n'a pas de note).
5. **La fiche prospect a fait son temps** : ses infos utiles ont migré vers l'entreprise/le
   client, et sa ligne d'index est déjà retirée (étape 4). Supprime-la, ou garde-la pour
   historique — mais ne la laisse pas dans `## À contacter`.

Montre toujours le plan de conversion (fichiers créés/modifiés) à l'utilisateur avant d'exécuter.

## Abandonner un prospect (hors cible, trop gros, doublon…)

Ne supprime pas, **archive** — c'est la convention du coffre pour ne pas le re-prospecter par
erreur :

1. Déplace la fiche dans `Prospects/Archive/` et passe `statut: À oublier`.
2. Dans `Prospects.md`, déplace sa ligne sous `## Archive`, **en gras et sans wikilink**
   (le lien mort est volontaire), en indiquant **le motif** :
   `- **Nom Entreprise** — trop gros` (ou « hors cible », « homonyme »…). Le motif est
   obligatoire : c'est lui qui évite la re-prospection.
3. **Recalcule le compteur d'en-tête.**

## Vérification

`python3 "$EXO" get "<nom>" --vault "$VAULT"` doit renvoyer un YAML valide ; après conversion,
`python3 "$EXO" links "<Prénom NOM>" --vault "$VAULT"` doit montrer le lien entreprise dans les
deux sens, et le prospect ne doit plus apparaître dans `Prospects.md`.
