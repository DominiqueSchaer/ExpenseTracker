# Repository Guidelines

## Project Structure & Module Organization
- `backend/` FastAPI service: `app/models.py` for ORM, `app/schemas.py` for Pydantic, `app/routers/` for endpoints, and `migrations/` for Alembic history. Docker and Procfile live at the directory root.
- `frontend_next/` Next.js 15 UI: pages in `src/app/`, shared client logic in `src/lib/api.ts`, and Tailwind styles in `src/app/globals.css`.
- `frontend-htmx/` holds the HTMX prototype; Tailwind builds from `static/styles.css` into `static/output.css`, also used by the root `index.html`.
- Secrets stay in `backend/.env`; UI configs belong in `.env.local` (e.g. `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`). Keep production credentials out of git.

## Build, Test, and Development Commands
- Backend setup: `cd backend && python -m venv .venv && .\.venv\Scripts\activate && pip install -r requirements.txt`. Run locally with `uvicorn app.main:app --reload --port 8000`.
- Database upgrades via `alembic upgrade head`; create migrations using `alembic revision --autogenerate -m "add expenses status"` after adjusting models.
- Frontend (Next): `cd frontend_next && npm install`, then `npm run dev`, `npm run build`, and `npm run lint`.
- HTMX skin: `cd frontend-htmx && npm install`; watch Tailwind with `npm run dev:css`, or build once with `npm run build:css`.

## Coding Style & Naming Conventions
- Python code is 4-space indented, fully typed, and keeps money in `Decimal`; reuse helpers like `schemas.chf` and return Pydantic models from routers. Name new routers `routers/<resource>.py` and functions with clear verbs.
- Pull database URLs from settings (`app/db.py`, `settings.py`) instead of hard-coding; acquire sessions through the `get_db` dependency.
- TypeScript uses PascalCase components, camelCase helpers, and the shared `api` client. Keep enum strings aligned with the backend before changing `ExpenseDto`.

## Testing Guidelines
- Add backend tests under `backend/tests/` with `pytest` + `pytest-asyncio` to cover happy-path, conflict, and not-found cases for each route.
- Frontend changes should run `npm run lint`; add unit coverage with Vitest/RTL or document interactive flows via Storybook. Capture edge cases such as mismatched status values.
- Before opening a PR, ping `/health` on the API and smoke-test any UI surface affected.

## Commit & Pull Request Guidelines
- Commit messages follow the short, imperative style seen in history (`add expense summary`, `fix router guard`); keep to one logical change per commit.
- PRs must list executed commands/tests, note new env vars or migrations, and include screenshots or API contract notes when relevant.
