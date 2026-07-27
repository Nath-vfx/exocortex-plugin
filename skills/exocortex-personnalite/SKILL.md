---
name: exocortex-personnalite
description: >
  Recherche et écriture dans le dossier Personnalité/ du coffre Exocortex : les notes
  sur LE PROPRIÉTAIRE du coffre lui-même (pas ses clients). On y trouve sa fiche hub
  « Qui suis-je » (identité, contact pro, métier/activité, régime fiscal, façon de
  travailler) et sa fiche « Style rédactionnel » (ton, tournures, structure de ses
  emails). Utilise ce skill pour retrouver une info perso du propriétaire (email, tel,
  LinkedIn, Calendly, métier, process, tarifs), et SURTOUT pour RÉDIGER un message qui
  sonne comme lui — email client, devis, relance, point projet : consulte alors la fiche
  Style rédactionnel pour reproduire sa voix. Déclenche sur « qui suis-je / mes infos /
  mon métier / mon process », « écris/rédige dans mon style / ma voix / comme moi », « un
  mail à tel client de ma part », « mon ton ». Pour une info sur un client ou une
  entreprise, utilise plutôt exocortex-clients / -entreprises / -prospects.
---

# Exocortex — Personnalité

Le dossier `Personnalité/` est la connaissance que l'Exocortex a de **son propriétaire** :
qui il est, comment il travaille, et comment il s'exprime. C'est un hub évolutif. Deux
usages : répondre à une question perso, et — le plus précieux — **écrire à sa place dans
sa voix**.

Localise le coffre et son mode d'accès via `${CLAUDE_PLUGIN_ROOT}/references/acces-coffre.md`,
puis utilise le script partagé `${CLAUDE_PLUGIN_ROOT}/scripts/exo.py`.

## Lister et lire les fiches perso

```bash
EXO="${CLAUDE_PLUGIN_ROOT}/scripts/exo.py"
ls "$VAULT/Personnalité/"
python3 "$EXO" get "Qui suis-je"            --vault "$VAULT"   # fiche hub : identité, contact, activité
python3 "$EXO" get "Style rédactionnel"     --vault "$VAULT"   # référentiel de la voix du propriétaire
```

La fiche « Qui suis-je » est le **hub** : son frontmatter (`type: personne`) porte les
coordonnées (email, téléphone, site, LinkedIn, Calendly) et son corps détaille l'activité,
le régime fiscal et la façon de travailler. Sa section « Sous-fiches me concernant » liste
en wikilinks les autres notes perso (parcours, compétences, offres & tarifs… à venir).

## Répondre à une question sur le propriétaire

Cible le champ ou la section utile (coordonnées dans le frontmatter du hub ; méthode/tarifs
dans le corps ou une sous-fiche dédiée). N'invente jamais : si l'info n'est pas encore dans
`Personnalité/`, dis-le et propose de l'y ajouter.

## Rédiger un message dans sa voix (usage clé)

Dès qu'on te demande d'écrire un email, un devis, une relance ou un point projet « de sa
part » / « dans son style », **ouvre et lis entièrement la fiche `Style rédactionnel`**
avant de rédiger — c'est la source de vérité de sa voix. N'apporte aucun ton, aucune
formule ou marqueur « par défaut » : la personnalité vit dans cette fiche, pas dans ce
skill. Applique fidèlement ce qu'elle décrit — et seulement ça :

- Le **niveau d'adresse** (tutoiement / vouvoiement) et le registre qu'elle fixe.
- Les **ouvertures, clôtures et signature** qu'elle donne, telles quelles.
- La **structure type** et le **mini-modèle réutilisable** s'ils y figurent.
- Les **mentions métier récurrentes** (modalités de paiement, mentions légales, TVA…) qu'elle
  liste — sans en inventer.

Appuie-toi sur les **exemples authentiques** de la fiche et adapte le registre au contexte
(livraison enthousiaste / financier carré / friction factuel mais courtois / relance
déculpabilisante). Si la fiche `Style rédactionnel` n'existe pas encore, dis-le et propose
de la créer plutôt que de deviner une voix. Si le message s'adresse à un client connu,
récupère ses infos via exocortex-clients pour personnaliser (prénom, projet en cours).

## Ajouter une sous-fiche perso

Range tout nouveau fichier perso dans `Personnalité/`, puis **branche-le au hub** : ajoute son
wikilink dans la section « Sous-fiches me concernant » de « Qui suis-je » (sinon il reste
orphelin). Frontmatter selon la nature : `type: personne` pour une fiche d'identité/bio,
`type: référentiel` pour un document de référence (comme le style). Conserve les clés du
frontmatter, dates `AAAA-MM-JJ`, téléphone entre guillemets. Montre le projet de fiche au
propriétaire avant d'enregistrer.

## Vérification

`python3 "$EXO" get "<fiche>" --vault "$VAULT"` doit renvoyer un YAML valide, et toute
nouvelle sous-fiche doit apparaître en wikilink dans « Qui suis-je » (`python3 "$EXO" links
"Qui suis-je" --vault "$VAULT"`).
