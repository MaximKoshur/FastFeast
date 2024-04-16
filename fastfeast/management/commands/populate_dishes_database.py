from django.core.management import BaseCommand
from fastfeast.models import CategoryDishes, Dishes, Institution
import json


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--data_file_path', type=str, required=False, default="fastfeast/management/commands/dishes.json")

    def handle(self, *args, **options):
        Dishes.objects.all().delete()
        CategoryDishes.objects.all().delete()
        file = options['data_file_path']
        with open(file) as f:
            file_content = f.read()
            templates = json.loads(file_content)
        for a in templates:
            cat1 = CategoryDishes.objects.create(name=a, parent=None)
            for b in templates[a]:
                cat2 = CategoryDishes.objects.create(name=b, parent=cat1)
                for c in templates[a][b]:
                    dish = Dishes.objects.create(category=cat2, name=templates[a][b][c].get('name'), description=templates[a][b][c].get('description'), price=templates[a][b][c].get('price'), institution=Institution.objects.get(name=templates[a][b][c].get('institution')))

