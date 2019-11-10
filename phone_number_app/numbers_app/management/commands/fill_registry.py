import requests
import typing

from django.core.management.base import BaseCommand

from numbers_app.models import RegistryEntry


REGISTRY_INFO_URLS = (
    "https://rossvyaz.ru/data/ABC-3xx.csv",
    "https://rossvyaz.ru/data/ABC-4xx.csv",
    "https://rossvyaz.ru/data/ABC-8xx.csv",
    "https://rossvyaz.ru/data/DEF-9xx.csv",
)
BATCH_SIZE = 10000
REGISTRY_DATA_FORMAT = ("code", "min_number", "max_number", "capacity", "operator", "region")


class Command(BaseCommand):
    def handle(self, *args, **options):
        for url in REGISTRY_INFO_URLS:
            self.stdout.write(f"Downdloading {url} file...")
            r = requests.get(url)
            self.stdout.write(self.style.SUCCESS("Successfully downloaded file! Start writing..."))

            current_start_i = 0
            entries = []

            for i, line in enumerate(r.iter_lines()):
                row = line.decode("utf-8").split(";")
                entries.append(RegistryEntry(**dict(zip(REGISTRY_DATA_FORMAT, row))))

                if len(entries) == BATCH_SIZE:
                    self._handle_batch_insert(entries, current_start_i, i)
                    entries = []
                    current_start_i = i + 1

            if entries:
                self._handle_batch_insert(entries, current_start_i, i)

            self.stdout.write(self.style.SUCCESS("Successfully inserted entries from file"))

        self.stdout.write(self.style.SUCCESS("Successfully done registry fill"))

    def _handle_batch_insert(self, entries, start_i, end_i):
        self.stdout.write(f"Insetrtig entries from {start_i} to {end_i}")
        RegistryEntry.objects.bulk_create(entries, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS("Successfully inserted entries"))
