# Administration guide

Staff and counselors use **Administration** (`/administration/`) after signing in with an account that has the right permissions (typically Django staff / counselor group).

## Control panel

The admin home links to:

| Module | Purpose |
|--------|---------|
| Manage Career Test | RIASEC questions and interest / program mappings |
| Manage Personality Test | Big Five items |
| Manage IQ Test | Visual / rich-text questions and choices |
| Manage Users | Search accounts; grant or revoke counselor access |
| Statistics | Aggregate charts for career, personality, and IQ |
| Manage Organization | Education levels, year levels, departments, programs |

Django’s built-in admin remains at `/admin/` for low-level model editing.

## Organization

1. Select an **education level**.
2. Manage **year levels** for that level.
3. Add or remove **departments**; open a department to manage **programs**.

Keep codes unique; they are used in forms and related records.

## Users

- Search by username and filter by join date.
- Open a student profile from the list.
- Use **Change permission** to make or remove counselors.

## Test content

Each manage-questions screen supports add / edit / delete flows (modals + HTMX where applicable).

- Prefer compressed images for IQ items (Quill + server-side helpers).
- Re-run `python manage.py compress_iq_images` if migrating large legacy base64 images.

## Statistics

Use the Career, Personality, and IQ tabs with department / program / date filters to explore cohort results. Charts render with Chart.js.

## Safety

- Destructive deletes (questions, departments, programs) confirm in modals — they may cascade to related data.
- Prefer staging fixtures before bulk edits in production.
