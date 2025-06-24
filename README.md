# Dépôts Sauvages - Protect Envi

Application de signalement des dépôts sauvages destinée aux communes.

Documentation disponible en :

- 🇫🇷 [Français](README)
- 🇬🇧 [English](README.en.md)

## 📑 Sommaire

- [🚀 Démarrage rapide avec Docker](#-démarrage-rapide-avec-docker)
- [🐳 Remarque sur Docker Compose](#-remarque-sur-docker-compose)
- [⚙️ Configuration de l'environnement](#️-configuration-de-lenvironnement)
- [🔧 Installation sans Docker](#-installation-sans-docker)
  - [Backend Django](#backend-django)
  - [Frontend Vue.js](#frontend-vuejs)
- [🗂️ Structure du projet](#️-structure-du-projet)
- [🛠️ Commandes Docker](#️-commandes-docker)
  - [Backend](#backend)
  - [Frontend](#frontend)
  - [Les deux conteneurs](#les-deux-conteneurs)

---

## 🚀 Démarrage rapide avec Docker

Lancez le projet en local à l'aide de Docker et Docker Compose V2 :

```bash
git clone https://github.com/your-username/depots-sauvages.git
cd depots-sauvages

docker compose up --build
```

Accès local :

- Frontend : [http://localhost:5173](http://localhost:5173)
- Backend : [http://localhost:8000](http://localhost:8000)
- Admin : [http://localhost:8000/admin/](http://localhost:8000/admin/)

  - utilisateur : admin
  - mot de passe : admin

- API : [http://localhost:8000/api/](http://localhost:8000/api/)

---

## 🐳 Remarque sur Docker Compose

Ce projet nécessite Docker Compose V2. Si vous utilisez Docker Compose V1, vous pouvez rencontrer des problèmes à la compilation.
Vérifiez votre version :

```bash
docker-compose --version  # V1 format
docker compose --version  # V2 format
```

### Si vous utilisez Docker Compose V1

Nous recommandons de faire une montée de version vers Docker Compose V2.
Sinon, vous pouvez utiliser cette commande :

```bash
docker-compose up --build
```

---

## ⚙️ Configuration de l'environnement

Copiez le fichier d'exemple :

```bash
cp .env.example .env
```

Note: Le fichier `.env` contient des variables pour Django et Vite. Les variables préfixées `VITE_` sont utilisées côté frontend.

---

## 🔧 Installation sans Docker

### Pré-requis

- Python 3.8+
- pipenv
- Node.js 20+ et Yarn
- PostgreSQL en prod
- SQLite en dev local

### 🔧 Configuration du Backend

1. Installez les dépendances avec pipenv :

```bash
pipenv install
```

2. Activez l’environnement virtuel :

```bash
pipenv shell
```

3. Exécutez les migrations :

```bash
python manage.py migrate
```

4. Créez un super-utilisateur si nécessaire :

```bash
python manage.py createsuperuser
```

5. Lancez le serveur de développement :

```bash
python manage.py runserver
```

Le back-end Django sera désormais accessible à l’adresse : [http://localhost:8000](http://localhost:8000)

### 🔧 Configuration du Frontend (Vue.js)

1. Accédez au répertoire `frontend` :

```bash
cd frontend
```

2. Installez les dépendances :

```bash
yarn install
```

3. Lancez le serveur de développement :

```bash
yarn dev
```

Le frontend Vue.js sera désormais accessible à l’adresse : [http://localhost:5173](http://localhost:5173)

---

## 🗂️ Structure du projet

```
depots-sauvages/
├── backend/        # Django backend
│   ├── settings/   # Django configuration
│   └── urls.py     # URL principale de configuration
├── frontend/       # Vue.js front-end
├── scripts/        # Scripts utilitaires
├── documents/      # Documents générés
```

---

## 🔒 Sécurité

### Limitation de débit - Throttling

- **IP throttling** : Limitation du nombre de requêtes par adresse IP
- **Email throttling** : Protection contre l'envoi massif d'emails
- Configuration via `backend/throttling/throttles.py`

### Timer anti-spam

Prévention des soumissions automatisées trop rapides.

- Vérification du temps minimum entre les soumissions
- Configuration : `MIN_FORM_TIME` en seconde
- Protection du formulaire signalement et l'envoie d'email
- Session-based\*\* : Timer lié à la session utilisateur

---

## 🛠️ Commandes Docker

### Conteneur backend

```bash
# Démarrer le serveur de développement
docker compose up backend

# Lancer Gunicorn pour une exécution proche de la production
docker compose run --rm backend gunicorn

# Exécuter des commandes Django
docker compose run --rm backend python manage.py [commande]

# Exemple : créer un superutilisateur
docker compose run --rm backend python manage.py createsuperuser

# Ouvrir un shell bash dans le conteneur
docker compose run --rm backend sh

```

### 🎨 Conteneur Frontend

```bash
# Démarrer le serveur de développement
docker compose up frontend

# Construire l'application pour la production
docker compose run --rm frontend build

# Lancer le serveur de prévisualisation
docker compose run --rm frontend preview

# Exécuter une commande yarn
docker compose run --rm frontend yarn [commande]

# Ouvrir un shell dans le conteneur
docker compose run --rm frontend sh
```

### Lancer les deux conteneurs

```bash
# Démarrer les deux conteneurs
docker compose up

# Construire et démarrer les deux conteneurs
docker compose up --build

# Arrêter tous les conteneurs
docker compose down
```
