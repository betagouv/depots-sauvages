# Dépôts Sauvages - Protect Envi

Application de signalement des dépôts sauvages destinée aux communes.

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
- [🧪 Tests](#-tests)
- [✨ Fonctionnalités](#-fonctionnalités-clés)
- [⚖️ Licence](#️-licence)

---

## ✨ Fonctionnalités

### Mes Dossiers

La page "Mes dossiers" permet aux utilisateurs connectés de consulter l'état de leurs procédures en cours.
Les données - numéro de dossier, date de dépôt, état d'avancement, sont récupérées **en temps réel** depuis l'API Démarches Numériques, c'est à dire qu'on ne stocke pas les données à cette étape-là.

### Téléchargement des documents

Une page de récupération des documents permet aux utilisateurs de télécharger un rapport de constatation et une lettre d'information.
Ces documents sont générés sur la base des données récupérées depuis l'API Démarches Numériques. Il y a un stokage local des données pour faciliter le traitement de génération des documents.

L'accès à cette page est restreint au propriétaire du dossier.

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
├── backend/             # Django backend
│   ├── settings/        # Django configuration
│   ├── dn_signalements/ # Signalements fais via Démarches Numériques
│   ├── signalements/    # Core : Modèles abstraits et mixins partagés
│   └── urls.py          # URL principale de configuration
├── frontend/            # Vue.js front-end
├── scripts/             # Scripts utilitaires
├── documents/           # Documents générés
```

---

## 📘 Conventions de langue

Ce projet est francophone et s'adresse à des utilisateurs finaux en France.
Pour assurer la lisibilité et la cohérence, nous appliquons les règles suivantes :

- Le code technique en anglais : fonctions, classes, composants UI réutilisables, commentaires.

- La logique métier en français : modèles de données, noms de composants liés aux procédures administratives, messages utilisateur : en français.

- L'interface utilisateur et la documentation fonctionnelle sont en français.

- Les commentaires dans le code sont en anglais.

- Les PRs et leurs descriptions sont en français.

Certaines notions intermédiaires comme « étape » peuvent relever du métier ou de la technique. Ici, nous utilisons « EtapeXForm.vue » (et non « StepXForm.vue ») car ces étapes correspondent à des phases du parcours utilisateur, et non à des composants techniques abstraits.

---

## 🧪 Tests

Pour plus de détails sur la stratégie de test et les commandes d'exécution, consultez le fichier [TESTING.md](./TESTING.md).

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

---

## ⚖️ Licence

Ce projet est sous licence libre **GNU Affero General Public License v3 (AGPL-3.0)**. Pour plus de détails, veuillez consulter le fichier [LICENSE.md](file:///home/sylvain/Dev/depots-sauvages/LICENSE.md) à la racine du dépôt.


