# Security Policy

## Supported versions

Security fixes are applied on the active `main` branch of this repository.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security problems.

Email the maintainers with:

- A short description of the issue
- Steps to reproduce or a proof of concept
- Impact assessment (e.g. auth bypass, XSS, data exposure)
- Your preferred contact for follow-up

Use the GitHub account or institutional contacts listed on the repository profile when possible.

We will acknowledge receipt when we can and work on a fix. Please give reasonable time before any public disclosure.

## Safe handling of secrets

- Never commit `.env`, API keys, SMTP passwords, or session cookie dumps
- Rotate credentials if they were ever committed or shared
- Use App Passwords for Gmail SMTP; do not use personal account passwords in config

## Known hardening notes

- Local/dev defaults (weak DB password, bootstrap superuser) are for convenience only — change them outside personal sandboxes
- Set a unique `SECRET_KEY` for every deployed environment
