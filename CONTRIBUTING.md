# Contributing

Thanks for helping improve PsytestJMC.

## Ways to contribute

- Bug reports and fixes
- Documentation improvements
- UI/UX polish that matches existing admin and public patterns
- Tests for assessment scoring and admin flows

## Development setup

Follow [docs/development.md](docs/development.md). Prefer Docker Compose so Postgres and seed data match other contributors.

## Branching and commits

1. Create a branch from `main`: `git checkout -b fix/short-description`
2. Keep commits focused; write clear messages (why over what).
3. Do not commit `.env`, secrets, `venv/`, `__pycache__/`, or local dumps (`cookies.txt`, HTML captures).

## Pull requests

- Fill out the PR template.
- Describe the user-facing impact and how you tested.
- Run before requesting review:

  ```bash
  python manage.py check
  python manage.py test
  ```

- Match existing template/CSS conventions (teal admin shell, shared `admin-manage` patterns for staff pages).

## Code style

- Python: follow surrounding Django style; keep views thin where patterns already do.
- Templates: prefer extending existing bases; reuse `admin-manage-*` / `admin-modal` classes for admin UI.
- Avoid drive-by refactors unrelated to the PR.

## Issues

Use GitHub Issues for bugs and feature requests. Include steps to reproduce, expected vs actual behavior, and environment (Docker vs venv, OS, browser).
