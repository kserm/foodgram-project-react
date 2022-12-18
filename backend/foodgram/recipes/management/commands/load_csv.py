import csv
from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        file_path = f'{settings.BASE_DIR}/data/ingredients.csv'
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            for name, measurement_unit in data:
                try:
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
                except Exception:
                    print(f'Ингредиент {name} уже добавлен')
        self.stdout.write(self.style.SUCCESS('Данные загружены.'))
