---
name: exocortex-personnalite
description: >
  Recherche et écriture dans le dossier Personnalité/ du coffre Exocortex : les notes
  sur Nathan LUI-MÊME (pas ses clients). On y trouve sa fiche hub « Qui suis-je »
  (identité, contact pro, métier/activité chez Banan Agency, régime fiscal art. 293 B,
  façon de travailler) et sa fiche « Style rédactionnel » (ton, tournures, structure de
  ses emails). Utilise ce skill pour retrouver une info perso de Nathan (email, tel,
  LinkedIn, Calendly, métier, process, tarifs), et SURTOUT pour RÉDIGER un message qui
  sonne comme lui — email client, devis, relance, point projet : consulte alors la fiche
  Style rédactionnel pour reproduire sa voix. Déclenche sur « qui suis-je / mes infos /
  mon métier / mon process », « écris/rédige dans mon style / ma voix / comme moi », « un
  mail à tel client de ma part », « mon ton ». Pour une info sur un client ou une
  entreprise, utilise plutôt exocortex-clients / -entreprises / -prospects.
---

# Exocortex — Personnalité

Le dossier `Personnalité/` est la connaissance que l'Exocortex a de **Nathan** : qui il
est, comment il travaille, et comment il s'exprime. C'est un hub évolutif. Deux usages :
répondre à une question perso, et — le plus précieux — **écrire à sa place dans sa voix**.

Localise le coffre comme dans le skill `exocortex` (Étape 0) et utilise le script partagé
`${CLAUDE_PLUGIN_ROOT}/scripts/exo.py`.

## Lister et lire les fiches perso

```bash
EXO="${CLAUDE_PLUGIN_ROOT}/scripts/exo.py"
ls "$VAULT/Personnalité/"
python3 "$EXO" get "Qui suis-je"            --vault "$VAULT"   # fiche hub : identité, contact, activité
python3 "$EXO" get "Style rédactionnel"     --vault "$VAULT"   # référentiel de la voix de Nathan
```

La fiche « Qui suis-je » est le **hub** : son frontmatter (`type: personne`) porte les
coordonnées (email, téléphone, site, LinkedIn, Calendly) et son corps détaille l'activité,
le régime fiscal et la façon de travailler. Sa section « Sous-fiches me concernant » liste
en wikilinks les autres notes perso (parcours, compétences, offres & tarifs… à venir).

## Répondre à une question sur Nathan

Cible le champ ou la section utile (coordonnées dans le frontmatter du hub ; méthode/tarifs
dans le corps ou une sous-fiche dédiée). N'invente jamais : si l'info n'est pas encore dans
`Personnalité/`, dis-le et propose de l'y ajouter.

## Rédiger un message dans la voix de Nathan (usage clé)

Dès qu'on te demande d'écrire un email, un devis, une relance ou un point projet « de la
part de Nathan » / « dans son style », **ouvre et lis entièrement la fiche
`Style rédactionnel — Nathan`** avant de rédiger — elle est riche et c'est la source de
vérité. Applique ses marqueurs :

- **Tutoiement** systématique avec le client ; chaleureux et pédagogique.
- **Ouverture** : « Salut [Prénom], » (par défaut) ou « Bonjour [Prénom], » (premier
  contact / sujet sensible), puis une phrase de lien (« J'espère que tu vas bien ! »).
- **Annonce positive** en tête (« Bonne nouvelle : … », « Comme convenu, je reviens vers
  toi avec… »).
- **Le « on » de la co-construction** et **toujours le pourquoi** de chaque point (étiquettes
  deux-points qui expliquent le bénéfice client).
- **Clôture** : disponibilité (« N'hésite pas… je reste dispo ») + signature **« Nathan »**
  seul, avec la formule adaptée (« À très vite, » / « À vendredi, » ; « Bien à toi, » pour
  un cadrage ou une relance de paiement).
- Mentions métier utiles : devis puis acomptes, **règlement par virement**, **« TVA non
  applicable, art. 293 B du CGI »**.

La fiche contient un **mini-modèle réutilisable** et des **exemples authentiques** : appuie-toi
dessus, et adapte le registre au contexte (livraison enthousiaste / financier carré / friction
factuel mais courtois / relance déculpabilisante). Si le message s'adresse à un client connu,
récupère ses infos via exocortex-clients pour personnaliser (prénom, projet en cours).

## Ajouter une sous-fiche perso

Range tout nouveau fichier perso dans `Personnalité/`, puis **branche-le au hub** : ajoute son
wikilink dans la section « Sous-fiches me concernant » de « Qui suis-je » (sinon il reste
orphelin). Frontmatter selon la nature : `type: personne` pour une fiche d'identité/bio,
`type: référentiel` pour un document de référence (comme le style). Conserve les clés du
frontmatter, dates `AAAA-MM-JJ`, téléphone entre guillemets. Montre le projet de fiche à
Nathan avant d'enregistrer.

## Vérification

`python3 "$EXO" get "<fiche>" --vault "$VAULT"` doit renvoyer un YAML valide, et toute
nouvelle sous-fiche doit apparaître en wikilink dans « Qui suis-je » (`python3 "$EXO" links
"Qui suis-je" --vault "$VAULT"`).
