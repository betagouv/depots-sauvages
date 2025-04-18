# Dépots Sauvages - Protect Envi

Application de signalement des dépôts sauvages pour les communes.

## Environment Setup

Copy the example environment file:

```bash
cp .env.example .env
```

Note: The `.env` file contains both Django backend and Vite frontend configurations. Variables prefixed with `VITE_` are exposed to the frontend application.

## Project Setup

### Prerequisites

- Python 3.8+
- pipenv
- Node.js and Yarn
- PostgreSQL in prod
- SQLite in local dev

### Backend Setup

1. Install dependencies using pipenv:

```bash
pipenv install
```

2. Activate the virtual environment:

```bash
pipenv shell
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

The Django backend will now be running at http://localhost:8000.

### Frontend Setup (Vue.js)

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
yarn install
```

3. Run the development server:

```bash
yarn dev
```

The Vue.js frontend will now be running at http://localhost:5173.

## Project Structure
