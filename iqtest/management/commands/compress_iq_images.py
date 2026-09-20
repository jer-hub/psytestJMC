from django.core.management.base import BaseCommand

from iqtest.models import Choice, Question
from iqtest.quill_images import compress_quill_json


class Command(BaseCommand):
    help = "Recompress base64 images embedded in IQ Quill question/choice fields."

    def add_arguments(self, parser):
        parser.add_argument(
            "--max-side",
            type=int,
            default=900,
            help="Max width/height in pixels (default: 900).",
        )
        parser.add_argument(
            "--quality",
            type=int,
            default=72,
            help="JPEG quality 1-95 (default: 72).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report savings without writing changes.",
        )

    def handle(self, *args, **options):
        max_side = options["max_side"]
        quality = options["quality"]
        dry_run = options["dry_run"]

        saved = 0
        bytes_before = 0
        bytes_after = 0

        def process(obj, field_name):
            nonlocal saved, bytes_before, bytes_after
            field = getattr(obj, field_name)
            raw = field.json_string if hasattr(field, "json_string") else str(field)
            before = len(raw.encode("utf-8"))
            compressed = compress_quill_json(
                raw, max_side=max_side, jpeg_quality=quality
            )
            after = len(compressed.encode("utf-8"))
            bytes_before += before
            bytes_after += after
            if compressed != raw:
                saved += 1
                if not dry_run:
                    setattr(obj, field_name, compressed)
                    obj.save(update_fields=[field_name])

        for question in Question.objects.all().iterator():
            process(question, "question")

        for choice in Choice.objects.all().iterator():
            process(choice, "choice")

        delta_kb = (bytes_before - bytes_after) / 1024.0
        self.stdout.write(
            self.style.SUCCESS(
                f"{'Would update' if dry_run else 'Updated'} {saved} records. "
                f"Payload {bytes_before/1024:.1f}KB -> {bytes_after/1024:.1f}KB "
                f"({delta_kb:.1f}KB saved)."
            )
        )
