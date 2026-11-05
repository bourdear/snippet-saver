# Snippet Saver

A small Django app for saving code snippets. You can list, create, view, edit, and delete snippets, each with a title, language, and code.

**Tech:** Django 5.2, server-rendered templates, Postgres 17, Docker Compose, pytest, and GitHub Actions.

> **Local use only:** the app has no user accounts, so anyone who can open it can edit or delete any snippet. Docker Compose only exposes it on your own machine. Add logins and production settings before putting it online.

## Setup

You'll need [Docker](https://www.docker.com/products/docker-desktop/) running. To run Django directly on your machine (Option 2), you'll also need Python 3.10 or newer.

```bash
git clone https://github.com/bourdear/snippet-saver.git
cd snippet-saver
cp .env.example .env
```

The values in `.env.example` are placeholders that work for local development. `.env` is ignored by Git, so keep any real secrets there.

## Run the app

Choose one option. Both use the same database, so your snippets show up in either one.

### Option 1: Everything in Docker

```bash
docker compose up --build
```

This starts Postgres, applies migrations, and starts Django. Code changes reload automatically.

### Option 2: Django on your machine, Postgres in Docker

```bash
docker compose up -d db
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

When you come back later, start Postgres with `docker compose up -d db`, activate the environment with `source .venv/bin/activate`, and run `python manage.py runserver`.

### Open the app

Either option serves the app at <http://localhost:8000>.

| Page | URL |
|---|---|
| All snippets | `/` |
| New snippet | `/new/` |
| Snippet details | `/<id>/` |
| Edit a snippet | `/<id>/edit/` |
| Delete a snippet | `/<id>/delete/` |
| Admin | `/admin/` |

## Admin access

The admin site needs a login, which you create once with one of these commands. It will ask you to choose a username and password.

```bash
# Option 1 (Docker)
docker compose exec web python manage.py createsuperuser

# Option 2 (on your machine)
python manage.py createsuperuser
```

## Run the tests

Postgres must be running, because the tests create a temporary test database there.

```bash
# Option 1 (Docker)
docker compose exec web pytest

# Option 2 (on your machine)
pytest
```

## Stop the app

```bash
docker compose down
```

Your snippets are kept in a Docker volume. Running `docker compose down -v` also **deletes that volume and all of your snippets**.

If you used Option 2, press `Ctrl+C` to stop Django first.

## Ports

| Service | Address | Notes |
|---|---|---|
| Django | `127.0.0.1:8000` | Only one server can use this port, so run one option at a time |
| Postgres | `127.0.0.1:5433` | Not 5432, to avoid clashing with a Postgres already on your machine. To change it, set `POSTGRES_PORT` in `.env` |

If you see `address already in use`, something else is using that port. For port 8000, that's often the server from the other option.

## Continuous integration

[GitHub Actions](.github/workflows/ci.yml) runs two jobs on every push:

- **test:** runs pytest against a Postgres 17 container
- **docker:** checks that the Docker image builds
