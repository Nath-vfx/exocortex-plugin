# Accès au coffre — étape 0 partagée

Référencée par les 5 skills. **Localise le coffre AVANT toute action**, et surtout
détermine le **mode d'accès** : il change la façon d'écrire. Ne code jamais un chemin en
dur.

## Cascade de localisation

Applique dans l'ordre, arrête-toi au premier qui répond :

1. **`$VAULT` déjà connu dans la session** → réutilise-le, ne recherche pas.
2. **Variable / cwd** : `EXOCORTEX_VAULT` est défini, ou un dossier parent du cwd contient
   `.obsidian` → **mode direct**. `exo.py` s'auto-détecte, tu peux l'appeler tel quel.
3. **Cowork sur l'appareil** :
   ```bash
   find /sessions/*/mnt -maxdepth 3 -name .obsidian -type d 2>/dev/null | head -1 | xargs dirname
   ```
   S'il renvoie un chemin → **mode direct** (lecture/écriture au shell).
4. **Session cloud (pas de `/sessions`)** : le coffre n'est joignable que par le **pont
   d'appareil**. Teste avec `device_list_dir` sur les dossiers connectés → **mode pont**.
5. **Rien ne répond** → dis à l'utilisateur que le coffre n'est pas joignable. **N'invente
   jamais un chemin** et n'écris nulle part.

Note le chemin trouvé comme `$VAULT`. Le script partagé vit dans le plugin, pas dans le
coffre : `EXO="${CLAUDE_PLUGIN_ROOT}/scripts/exo.py"`.

## Le mode conditionne l'écriture

| | Mode **direct** | Mode **pont** |
|---|---|---|
| Lecture | `exo.py`, `rg`, `Read` au shell | `device_bash`, ou mise en scène puis lecture locale |
| Écriture | `Edit`/`Write` au shell sur `$VAULT` | **`device_commit_files` uniquement**, avec `expectedMtimeMs` |
| `exo.py` | utilisable lecture **et** repère d'écriture | **lecture seule** (voir ci-dessous) |

**Mode pont — piège à éviter.** Les fichiers mis en scène (`device_stage_files`) arrivent
dans un espace **en lecture seule** (`/mnt/user-data/uploads/`). Le cycle correct est :
`device_stage_files` → copier ailleurs → éditer la copie → `SendUserFile` →
`device_commit_files` vers le chemin d'origine (avec `expectedMtimeMs` pour ne pas écraser
une modif faite dans Obsidian entre-temps). `exo.py` reste utilisable en **lecture** en
montant les fichiers puis en pointant `--vault` sur la copie — **mais jamais en écriture** :
sinon tu édites une copie éphémère en croyant modifier le coffre.

## Recenser la structure

Le coffre **grandit** (Projets, Devis, Contenu… en plus de Clients/Entreprises/Prospects/
Personnalité). Ne suppose jamais l'arborescence : recense-la avant d'agir.

```bash
python3 "$EXO" index --vault "$VAULT"     # type, nom, chemin de chaque fiche
```
