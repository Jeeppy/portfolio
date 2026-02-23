# 🚀 Portfolio

Self-hosted developer portfolio — FastAPI REST API + Vue.js 3 SPA | Docker + GitHub Actions CI/CD

## Tech Stack

| Layer        | Technology                                                                                                      |
| ------------ | --------------------------------------------------------------------------------------------------------------- |
| **Backend**  | [FastAPI](https://fastapi.tiangolo.com/) — Python 3.12                                                          |
| **Frontend** | [Vue.js 3](https://vuejs.org/) — TypeScript + [TailwindCSS](https://tailwindcss.com/)                           |
| **Database** | SQLite via [SQLModel](https://sqlmodel.tiangolo.com/) + [Alembic](https://alembic.sqlalchemy.org/) (migrations) |
| **Auth**     | JWT (single-user)                                                                                               |
| **Deploy**   | [Coolify](https://coolify.io/) (self-hosted PaaS) + Cloudflare Tunnels                                          |
| **CI/CD**    | GitHub Actions → Proxmox (self-hosted)                                                                          |

### Code Quality

| Tool                                             | Role                               |
| ------------------------------------------------ | ---------------------------------- |
| [Ruff](https://docs.astral.sh/ruff/)             | Linter + formatter                 |
| [mypy](https://mypy-lang.org/)                   | Static type checking               |
| [Bandit](https://bandit.readthedocs.io/)         | Security linter                    |
| [pytest](https://docs.pytest.org/) + pytest-cov  | Tests + coverage                   |
| [pip-audit](https://pypi.org/project/pip-audit/) | Dependency vulnerability scanner   |
| [pre-commit](https://pre-commit.com/)            | Git hooks (lint, format, security) |

## Prerequisites

- [pyenv](https://github.com/pyenv/pyenv) — Python version management
- [uv](https://docs.astral.sh/uv/) — Fast Python package manager
- [Node.js](https://nodejs.org/) ≥ 18 — For the Vue.js frontend
- [Docker](https://www.docker.com/) & Docker Compose — For containerized deployment

## Getting Started

### 1. Clone & configure

```bash
git clone git@github.com:YOUR_USER/portfolio.git
cd portfolio

cp .env.example .env
# Edit .env with your settings
```

### 2. Backend setup

```bash
cd backend

# Python version is automatically set via .python-version
pyenv install 3.12.8  # if not already installed

# Install dependencies
uv sync

# Apply database migrations
uv run alembic upgrade head

# Run the API (dev mode with hot reload)
uv run fastapi dev app/main.py
```

API available at http://localhost:8000
Interactive docs at http://localhost:8000/docs

### 3. Frontend setup

```bash
cd frontend

npm install
npm run dev
```

App available at http://localhost:5173

## Useful Commands

### Backend

```bash
cd backend

# Run API
uv run fastapi dev app/main.py

# Apply migrations
uv run alembic upgrade head

# Create a new migration (after model changes)
uv run alembic revision --autogenerate -m "description"

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type checking
uv run mypy app/

# Security scan (code)
uv run bandit -r app/

# Security scan (dependencies)
uv run pip-audit

# Tests with coverage
uv run pytest
```

### Git hooks

```bash
# Install pre-commit hooks (run once)
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

### Docker (dev)

```bash
# Build et lancer l'API
docker compose up --build

# En arrière-plan
docker compose up -d

# Logs
docker compose logs -f api

# Arrêter
docker compose down
```

## License

This project is licensed under the [MIT License](LICENSE).
