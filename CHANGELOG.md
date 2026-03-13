## [2026.3.1] - 2026-03-13

  ### 🐛 Bug Fixes

  - *(backend)* Set explicit UID/GID 9999 for appuser to fix volume permissions
  in production
  - *(backend)* Delete old file after successful upload, not before
  - *(frontend)* Replace deprecated Lucide brand icons with simple-icons
  - *(frontend)* Display error message on failed login
  - *(frontend)* Replace flag emojis with SVG using country-flag-icons
  - *(frontend)* Display upload errors in profile form with client-side
  validation
  - *(frontend)* Redirect to login on 401 in admin pages via adminFetch helper

## [2026.3.0] - 2026-03-12

### 🚀 Features

- Init FastAPI with projects endpoints
- Database setup with SQLModel + Project model
- Full CRUD with Pydantic schemas
- JWT auth with login and protected routes
- Profile and contact endpoints
- Add structured logging with structlog
- Add ?all=true query param to list unpublished projects as admin
- Add CORS middleware with configurable origins
- Add soft delete for contact messages
- Add pagination to contact messages list
- Add pagination to projects and contact messages list endpoints
- Add rate limiting on contact form endpoint
- Add global exception handler for unhandled errors
- Add pip-audit step to CI workflow
- Add health check endpoint and redirect root to /docs
- Add demo_url field to Project model and schemas
- Add Alembic for database migrations
- Extract social links from Profile into SocialLink model
- Add repository_url field to Project model
- Add project categories with filtering
- Replace avatar_url/resume_url with file upload endpoints
- Add alternance support to education model
- Add appointment booking system
- Add Docker support for backend
- CD staging deployment to CI workflow
- Add CD staging deployment to CI workflow
- Add CD production deployment to CI workflow
- Initialize Next.js 15 frontend project
- Add docker for frontend
- Add frontend service to docker-compose.prod.yml
- Add frontend CI/CD deploy jobs for staging and production
- Add public pages
- Configure Prettier for frontend code formatting
- Add ESLint and Prettier checks to pre-commit and CI
- Add public and admin skills endpoints
- Implement admin authentication flow (login, middleware, logout)
- Implement admin projects CRUD
- Add admin skills CRUD
- Add i18n support for public pages (fr/en)
- Style public pages (#122)
- Responsive nav with hamburger menu
- Style admin pages with Tailwind CSS
- CRUD admin expériences
- CRUD admin education
- Admin profile management
- Admin contact messages management
- Admin dashboard

### 🐛 Bug Fixes

- Auto-create database directory on startup
- Validate email fields with Pydantic EmailStr
- Add field length constraints and skill level range to schemas
- Correct type in CI runner label (ubuntu-lastest -> ubuntu-latest)
- Add required env variables to CI test step
- Use ContactRead as response model for conact create endpoint
- Hide unpublished projects from public get endpoint
- Add field length constraints to SQLModel table models
- Restrict allowed CORS methods and headers
- Update Project.updated_at on modification
- Use single rate limiter instance across the app
- Add bounds on pagination query parameters
- Strip whitespace on ContactCreate text fields
- Ensure test fixture cleanup with try/finally
- Replace == True with SQLAlchemy true() and remove E712 ignore
- Remove unused python-jose dependency (CVE-2024-23342)
- Backend review corrections
- Correct ghcr.io registry URL in CD workflow
- : minor backend corrections
- Run alembic migrations on container startup
- Split auth.ts into server and client modules

### 🚜 Refactor

- Project structure with routers and config
- Replace status code integers with FastAPI status constants
- Replace JSON strings with relational models
- Translate french comments, docstrings and API messages to English
- Use cascade delete-orphan for profile relations
- Extract _get_message_or_404 helper in contact router
- Use None instead of empty string for optional Profile fields
- Use None instead of empty string for optional model fields
- Split projects routes into public and admin routers
- Reorganize admin routes into app/routers/admin/
- Move LoginForm and LogoutButton to components/admin

### 📚 Documentation

- Add OpenAPI docstrings to all route functions
- Update README for Alembic migrations
- Add Coolify setup documentation
- Update Coolify setup with production environment
- Update README and Coolify setup documentation
- Update README for Next.js 15 frontend

### ⚡ Performance

- Add missing indexes on foreign keys and filters

### 🧪 Testing

- Add unit tests for all endpoints
- Add edge case tests for contact and project slugs
- Add missing edge case tests

### ⚙️ Miscellaneous Tasks

- Init project with .gitignore and .env.example
- Project setuf - uv, ruff, mypy, bandit, pytest-cov, pre-commit, pip-audit
- Add format and safety hooks to pre-commit config
- Add GitHub Actions workflow for backend
- Standarize logging across all routers
- Tighten dependancy version constraints
- Add MIT LICENCE
- Add CODEOWNERS file
- Add security policy (SECURITY.md)
- Add issue and pull request templates
- Configure Dependabot for automated dependency updates
