---
name: exocortex-entreprises
description: >
  Recherche et écriture des fiches ENTREPRISES du coffre Obsidian Exocortex de l'utilisateur
  (dossier Entreprises/, une note par société cliente). Utilise ce skill pour retrouver
  les infos légales et de facturation d'une société d'un client (SIRET/SIREN, TVA
  intracommunautaire, forme juridique, capital, code NAF, adresse, email de facturation,
  dirigeant), pour CRÉER une fiche entreprise, METTRE À JOUR un champ, ou gérer son lien
  vers le(s) client(s). Déclenche sur « les infos légales de telle société », « le SIRET/
  la TVA/l'adresse de facturation de telle entreprise », « qui dirige telle société »,
  « crée la fiche entreprise X ». Concerne uniquement les sociétés du portefeuille de
  l'utilisateur, PAS des entreprises tierces publiques (→ recherche web).
---

# Exocortex — Entreprises

Gère les fiches du dossier `Entreprises/` : une note Markdown par société cliente
(personne morale), avec frontmatter légal/facturation et un corps « Informations légales »
+ « Dirigeant ». Autonome : recherche ET écriture. Localise le coffre comme dans le skill
`exocortex` (Étape 0), utilise `${CLAUDE_PLUGIN_ROOT}/scripts/exo.py`, et lis les règles
d'or dans `${CLAUDE_PLUGIN_ROOT}/references/conventions.md` **avant d'écrire**.

## Rechercher une entreprise

```bash
EXO="${CLAUDE_PLUGIN_ROOT}/scripts/exo.py"
python3 "$EXO" get "QUALIROAD"     --vault "$VAULT"        # fiche entière
python3 "$EXO" field siret_siren   --vault "$VAULT"        # toutes les sociétés + SIRET
python3 "$EXO" links "M-Energies Pro" --vault "$VAULT"     # client(s) rattaché(s)
rg -l "\[\[M-Energies Pro\]\]" "$VAULT"                    # recherche inversée
```

Les détails légaux (forme juridique, capital, NAF, TVA, dates) sont souvent dans le
**corps** sous « Informations légales », pas seulement dans le frontmatter.

## Schéma d'une fiche entreprise

```yaml
---
type: entreprise
adresse: "12 rue …, 75000 Ville"   # guillemets (virgules)
téléphone:
email_facturation: contact@…
siret_siren: "940 852 932"
site_web:
clients:
  - "[[Prénom NOM]]"
source_notion:
---

# Nom Entreprise

## Informations légales

- **Forme juridique**, **SIREN**, **SIRET siège**, **TVA intracommunautaire**,
  **Capital social**, **Date de création**, **Activité (NAF)**, **Adresse**.

## Dirigeant

- [[Prénom NOM]] — Rôle (depuis …)
```

## Créer / mettre à jour — règles essentielles

1. **Nom de fichier = titre H1** (`Entreprises/Nom.md`), cible des wikilinks. Garde le nom
   commercial tel qu'employé par l'utilisateur.
2. **Conserve toutes les clés** du frontmatter, même vides.
3. **Lien bidirectionnel obligatoire.** `clients: [[Prénom NOM]]` côté entreprise doit
   répondre à `entreprises: [[Nom Entreprise]]` côté client. Crée la fiche client manquante
   si besoin (via exocortex-clients ou exocortex-prospects selon le statut).
4. **Édition chirurgicale.** Modifie la ligne concernée ; n'écrase pas le corps légal.
5. **Adresse/SIRET entre guillemets** s'ils contiennent virgule ou espaces significatifs.
6. **Source.** Les données légales viennent souvent de societe.com — cite la source dans le
   corps comme dans l'existant ; renseigne `source_notion` si la fiche vient de Notion.

Avant d'enregistrer, montre à l'utilisateur ce que tu vas écrire et où.

## Vérification

`python3 "$EXO" get "<entreprise>" --vault "$VAULT"` doit renvoyer un YAML valide, et le
lien client doit se répondre dans les deux sens (`links`).
