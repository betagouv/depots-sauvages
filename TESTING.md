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

Vue + Vitest

Situés dans `frontend/tests/`, ils testent les composants UI de manière isolée et l'accessibilité.

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

E2E - Playwright

Situés dans `e2e/`, ils simulent un utilisateur réel dans un vrai navigateur. Ils vérifient que le frontend communique bien avec le backend.

- **Outil** : [Playwright](https://playwright.dev/)
- **Lancer les tests** :
  ```bash
  # Installer les navigateurs (une seule fois)
  yarn playwright install
  # Lancer les tests
  yarn playwright test
  ```
- **Note** : L'application doit être lancée (`docker compose up`) ou Playwright tentera de la lancer lui-même via la commande configurée dans `playwright.config.ts`.
