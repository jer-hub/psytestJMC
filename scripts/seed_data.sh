#!/usr/bin/env sh
# Seed reference data in the correct order (fixtures preferred over CSV imports).
set -e

python manage.py loaddata data/fixtures/educationlevel.json
python manage.py loaddata data/fixtures/department.json
python manage.py loaddata data/fixtures/program.json
python manage.py loaddata data/fixtures/year.json
python manage.py loaddata data/fixtures/personalitytest_question.json
python manage.py loaddata data/fixtures/riasec_question.json
python manage.py loaddata data/fixtures/riasec_offeredprogram.json
python manage.py loaddata data/fixtures/iqtest_question.json
python manage.py loaddata data/fixtures/choice.json

echo "Fixtures loaded. Optional CSV imports (if regenerating from source):"
echo "  python manage.py import_educationlevel data/csv/edulvl.csv"
echo "  python manage.py import_department data/csv/department.csv"
echo "  python manage.py import_program data/csv/program.csv"
echo "  python manage.py import_year data/csv/year.csv"
echo "  python manage.py import_personality_question data/csv/personalitytest_question.csv"
echo "  python manage.py import_career_question data/csv/riasec_question.csv"
echo "  python manage.py import_offeredprogram data/csv/riasec_offeredprogram.csv"
echo "  python manage.py import_iq_question data/csv/iqtest_question.csv"
