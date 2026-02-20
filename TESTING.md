# Documentation des Tests

Ce projet utilise plusieurs types de tests pour assurer la qualité du code et la stabilité de l'application.

## 1. Tests Backend

Django + Pytest

Situés dans `backend/*/tests/`, ils testent la logique métier, les modèles et l'API.

- **Outil** : [Pytest](https://docs.pytest.org/)
- **Lancer les tests** :

  ```bash

  # Via Docker
  docker compose run --rm backend pytest

  # Avec pipenv
  pipenv run pytest
  ```

## 2. Tests Frontend

Vue + Vitest. Situés dans `frontend/tests/`

- **Outil** : [Vitest](https://vitest.dev/) + [Vue Test Library](https://testing-library.com/docs/vue-testing-library/intro/)
- **Lancer les tests** :
  ```bash
  # Installation préalable
  yarn install
  # Lancement
  yarn test
  # Ou via Docker
  docker compose run --rm frontend yarn test
  ```

## 3. Tests de Bout en Bout

E2E - Playwright. Situés dans `e2e/`

- **Outil** : [Playwright](https://playwright.dev/)
- **Lancer les tests** :

  ```bash
  # Via Docker (Recommandé)
  docker compose run --rm e2e

  # En local (nécessite l'installation des dépendances système)
  yarn playwright install
  yarn playwright test
  ```

- **Note** : En mode Docker, les tests s'exécutent contre les conteneurs `frontend` et `backend`. En local, Playwright tentera de lancer le serveur de développement lui-même.
