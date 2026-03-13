# Release Process

Processus complet depuis la branche feature jusqu'à la GitHub Release.

## 1. Créer la PR feature → develop

```bash
# Depuis la branche feature (ex: feat/136-parallelise-admin-fetch)
gh pr create \
  --base develop \
  --title "feat: description de l'issue" \
  --body "Closes #XXX"
```

Attendre que la CI passe (lint + test), puis merger via l'interface GitHub (**Squash and merge**).

---

## 2. Créer la PR de release develop → main

```bash
# S'assurer que develop est à jour localement
git checkout develop && git pull

# Générer le changelog (depuis le dernier tag)
git cliff --tag vX.Y.Z --unreleased

# Créer la PR
gh pr create \
  --base main \
  --head develop \
  --title "release: vX.Y.Z" \
  --body "Release vX.Y.Z"
```

> **Important :** Pour la PR de release, utiliser **Create a merge commit** (pas squash) afin de préserver l'historique pour git-cliff.

---

## 3. Bumper les versions et mettre à jour CHANGELOG.md

Éditer les fichiers de version, générer le changelog, puis commiter sur develop avant de merger la PR.

```bash
# backend/pyproject.toml → version = "X.Y.Z"
# (frontend/package.json ne supporte pas le format calendaire — ne pas modifier)

git cliff --tag vX.Y.Z --unreleased >> CHANGELOG.md
# Éditer CHANGELOG.md pour placer la nouvelle section en tête du fichier

git add backend/pyproject.toml CHANGELOG.md
git commit -m "chore(release): bump version to vX.Y.Z"
git push origin develop
```

> Le format de version est sans le `v` : `2026.3.0` (pas `v2026.3.0`).

---

## 4. Merger la PR develop → main

Merger via l'interface GitHub avec **Create a merge commit**.

---

## 5. Créer le tag et pusher

```bash
git checkout main && git pull
git tag vX.Y.Z
git push origin vX.Y.Z
```

---

## 6. Créer la GitHub Release

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z" \
  --notes "$(git cliff --tag vX.Y.Z --unreleased)"
```

Ou depuis l'interface GitHub : **Releases → Draft a new release → choisir le tag**.

---

## Numérotation des versions

Format : `vYYYY.MM.patch`

- `YYYY.MM` = année et mois de la release
- `patch` = incrément dans le mois (0, 1, 2…)

Exemples : `v2026.3.0`, `v2026.3.1`, `v2026.4.0`
