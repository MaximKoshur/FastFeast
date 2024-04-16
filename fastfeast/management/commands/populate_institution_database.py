from django.core.management import BaseCommand
from fastfeast.models import CategoryInstitution, Institution
import json


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--data_file_path', type=str, required=False, default="fastfeast/management/commands/institution.json")

    def handle(self, *args, **options):
        Institution.objects.all().delete()
        CategoryInstitution.objects.all().delete()
        file = options['data_file_path']
        with open(file) as f:
            file_content = f.read()
            templates = json.loads(file_content)
        for i in templates:
            c = CategoryInstitution.objects.create(name=i)
            for j in templates[i]:
                inst = Institution.objects.create(category=c, name=templates[i][j].get('name'), description=templates[i][j].get('description'), address=templates[i][j].get('address'))

