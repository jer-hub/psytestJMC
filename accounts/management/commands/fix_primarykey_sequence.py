from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Reset sequences for specified tables'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("BEGIN;")
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"accounts_educationlevel"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "accounts_educationlevel";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"accounts_department"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "accounts_department";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"accounts_program"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "accounts_program";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"accounts_year"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "accounts_year";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"auth_permission"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_permission";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"auth_group_permissions"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_group_permissions";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"auth_group"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_group";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"auth_user_groups"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_user_groups";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"auth_user_user_permissions"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_user_user_permissions";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"auth_user"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_user";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"iqtest_question"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "iqtest_question";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"iqtest_choice"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "iqtest_choice";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"personalityTest_question"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "personalityTest_question";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"personalityTest_recommendedprogram"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "personalityTest_recommendedprogram";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"riasec_offeredprogram"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "riasec_offeredprogram";"""
            )
            cursor.execute(
                """SELECT setval(pg_get_serial_sequence('"riasec_question"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "riasec_question";"""
            )
            cursor.execute("COMMIT;")
