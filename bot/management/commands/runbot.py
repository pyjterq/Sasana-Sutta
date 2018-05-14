# requests #(do pobierania)
# bs4 #(do parsowania)
import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from bot.models import Sutta
from bot.parser_html import get_link_list, get_sutta_data_list, SUTTA_LINKS


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('go')
        link_list = get_link_list(SUTTA_LINKS)
        # link_list = link_list[10:]
        data_list = get_sutta_data_list(link_list)
        # print(data_list)

        with transaction.atomic():
            save_sutta_list(data_list)

# MODEL:


# json.loads(sutta.content) -> buduje slownik z paragrafami

# Sutta -> to jest model (klasa mapujaca tabelke)

# SELECT * ...
# DELETE *. ..

# objects to inaczej obiekt klasy Manager

# Sutta.objects.create(...)

# Sutta.objects.filter(...)  # SELECT * FROM Sutta WHERE ...

# Sutta.objects.all() # SELECT * FROM Sutta;
#
# title = models.CharField(max_length=250)
#     url = models.URLField()
#     author = models.CharField(max_length=50)
#     collection = models.CharField(max_length=4)
#     sutta_nr = models.SmallIntegerField()
#     content = models.TextField()
#     created_at = models.DateTimeField()

def save_sutta_list(data_list):
    """Create Sutta instance list and save it"""
    for data in data_list:
        Sutta.objects.create(
            title=data['title'],
            title_pali=data['title_pali'],
            url=data['url'],
            content=json.dumps(data['paragraph_list']),
            author=data['author'],
            collection=data['collection'],
            sutta_nr=data['sutta_nr']
            # ... itd
        )
