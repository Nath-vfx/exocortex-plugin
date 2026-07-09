---
name: exocortex-prospects
description: >
  Gère le pipeline de PROSPECTION du coffre Obsidian Exocortex de Nathan : le dossier
  Prospects/ (une fiche par entreprise à démarcher, type "prospect") plus l'index
  Prospects.md. Chaque fiche porte le secteur, le statut (ex. "À contacter"), le contact,
  email, téléphone, le site actuel, un lien Loom et des notes d'analyse. Utilise ce skill
  pour LISTER/filtrer les prospects (par secteur ou statut), RETROUVER une info d'un
  prospect (téléphone, site actuel, lien Loom, notes), AJOUTER un prospect, METTRE À JOUR
  son statut/ses notes, et surtout le CONVERTIR en client quand il signe (créer sa fiche
  entreprise + sa fiche client, mettre à jour les index). Déclenche sur « ajoute un
  prospect », « mes prospects à contacter », « les prospects du secteur X », « le tel/site
  de tel prospect », « tel prospect a signé / convertis-le en client ». Pour un client déjà
  actif → exocortex-clients ; pour les infos légales d'une société → exocortex-entreprises.
---

# Exocortex — Prospects

Le dossier `Prospects/` est le pipeline de prospection de Banan Agency : **une fiche par
entreprise à démarcher** (refonte / création de site), regroupées par secteur dans l'index
`Prospects.md`. Une fiche prospect décrit une cible, pas encore un client. Autonome :
recherche ET écriture. Localise le coffre comme dans le skill `exocortex` (Étape 0) et
utilise `${CLAUDE_PLUGIN_ROOT}/scripts/exo.py` ; règles d'écriture dans
`${CLAUDE_PLUGIN_ROOT}/references/conventions.md`.

## Lister / filtrer les prospects

```bash
EXO="${CLAUDE_PLUGIN_ROOT}/scripts/exo.py"
python3 "$EXO" field statut  --vault "$VAULT" --value "À contacter"
python3 "$EXO" field secteur --vault "$VAULT" --value "Services"
python3 "$EXO" get "Coiffure Océane" --vault "$VAULT"     # fiche entière (floue)
```

L'index `Prospects.md` donne la vue d'ensemble groupée par secteur (BTP / PME – Commerce /
PME – Services) avec une ligne descriptive par prospect.

## Schéma d'une fiche prospect

```yaml
---
type: prospect
statut: À contacter        # cycle : À contacter → Contacté → RDV → Devis envoyé → Signé / Perdu
secteur: "PME – Services"  # BTP / PME – Commerce / PME – Services
contact:                   # nom de l'interlocuteur si connu
email:
téléphone: "03 81 39 00 85"
site_actuel: https://…     # site existant (souvent à refondre)
lien_loom:                 # vidéo Loom de prospection
source_notion: https://app.notion.com/p/…
---

# Nom Entreprise

## Notes

Analyse de la cible : activité, localisation, état du site actuel, angle d'approche.
```

## Ajouter un prospect

Crée `Prospects/Nom Entreprise.md` avec le schéma ci-dessus (renseigne ce qu'on a, garde les
clés vides sinon), puis **ajoute-le à l'index `Prospects.md`** sous le bon secteur, au format
existant : `- [[Nom Entreprise]] · Activité, Ville (dpt)`. Sans cette ligne d'index, le
prospect reste hors de la vue d'ensemble.

## Mettre à jour un prospect

Édition chirurgicale du frontmatter (ex. `statut: À contacter` → `Contacté` → `Devis envoyé`),
et puces datées dans `## Notes` pour l'historique d'approche. N'écrase pas les notes existantes.

## Convertir un prospect → client (quand il signe)

Le prospect (entreprise) devient un client. Reproduis le modèle Clients/ + Entreprises/ :

1. **Crée la fiche entreprise** `Entreprises/Nom Entreprise.md` (via exocortex-entreprises) à
   partir des infos prospect + données légales (SIRET, etc. — à compléter depuis societe.com).
2. **Crée la fiche client** `Clients/Prénom NOM.md` pour l'interlocuteur (le `contact`), via
   exocortex-clients : `statut: Client actif`, `date_début` = date de signature, `projet`,
   et `entreprises: [[Nom Entreprise]]`.
3. **Lien bidirectionnel** client ↔ entreprise (`clients: [[Prénom NOM]]` en retour).
4. **Mets à jour les index** : retire la ligne du prospect dans `Prospects.md` et ajoute le
   client sous « Clients actifs » dans `Clients.md` (format : `- [[Prénom NOM]] — [[Nom
   Entreprise]] · Projet`).
5. **Demande à Nathan** s'il veut supprimer/archiver la fiche `Prospects/Nom Entreprise.md`
   (ses infos utiles ont migré vers l'entreprise) ou la conserver pour historique.

Montre toujours le plan de conversion (fichiers créés/modifiés) à Nathan avant d'exécuter.

## Vérification

`python3 "$EXO" get "<nom>" --vault "$VAULT"` doit renvoyer un YAML valide ; après conversion,
`python3 "$EXO" links "<Prénom NOM>" --vault "$VAULT"` doit montrer le lien entreprise dans les
deux sens, et le prospect ne doit plus apparaître dans `Prospects.md`.
