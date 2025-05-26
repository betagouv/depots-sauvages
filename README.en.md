# Dépots Sauvages - Protect Envi

An application for reporting illegal and unauthorized waste dumping in public areas.

## Quick Start with Docker

Run the project locally using Docker and Docker Compose V2:

```bash
# Clone the repository
git clone https://github.com/your-username/depots-sauvages.git
cd depots-sauvages

# Start the application using Docker Compose V2
docker compose up --build
```

The application will be available at:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Admin interface: http://localhost:8000/admin/
  - user: admin
  - password: admin
- API: http://localhost:8000/api/

More details in `docker-compose.yml`.

### Docker Compose Version Note

This project uses Dockerfiles that are compatible with Docker Compose V2. If you're using an older version of Docker Compose V1, you might encounter errors when building the containers.

#### How to check your Docker Compose version:

```bash
docker-compose --version  # V1 format
docker compose --version  # V2 format
```

#### If you have Docker Compose V1

We recommend upgrading to Docker Compose V2:

Alternatively, you can use V1 with this syntax though you might encounter build issues:

```bash
docker-compose up --build
```

## Environment Setup

Copy the example environment file:

```bash
cp .env.example .env
```

Note: The `.env` file contains both Django backend and Vite frontend configurations. Variables prefixed with `VITE_` are exposed to the frontend application.

## Project Setup without Docker

### Prerequisites

- Python 3.8+
- pipenv
- Node.js 20+ and Yarn
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

4. Create a superuser if needed:

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

```
depots-sauvages/
├── backend/                    # Django backend
│ ├── settings/                 # Django settings
│ └── urls.py                   # Main URL configuration
├── frontend/                   # Vue.js frontend
├── scripts/                    # Helper scripts
├── documents/                  # App generated documents
```

## Docker Commands

### Backend Container

```bash
# Start the development server
docker compose up backend

# Run with Gunicorn for production-like
docker compose run --rm backend gunicorn

# Run Django management commands
docker compose run --rm backend python manage.py [command]

# Example: Create a superuser
docker compose run --rm backend python manage.py createsuperuser

# Open a bash shell in the container
docker compose run --rm backend sh
```

### Frontend Container

```bash
# Start the development server
docker compose up frontend

# Build for production
docker compose run --rm frontend build

# Run the preview server
docker compose run --rm frontend preview

# Run any yarn command
docker compose run --rm frontend yarn [command]

# Open a shell in the container
docker compose run --rm frontend sh
```

### Running Both Containers

```bash
# Start both containers
docker compose up

# Build and start both containers
docker compose up --build

# Stop all containers
docker compose down
```
