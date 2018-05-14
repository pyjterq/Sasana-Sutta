from django.core.management.base import BaseCommand, CommandError
from bot.models import Sutta
from bot.html import render_sutta

# AUTHOR_DIRS = [
#     # sciezki autorow
# ]

# SUTTA_OUTPUT_FILENAME = "output/{sutta_nr}.html"
SUTTA_OUTPUT_FILENAME = "pl/{author}/{sutta_nr}.html"


# def check_author_dirs():
#     pass


class Command(BaseCommand):
    """Klasa zawsze musi nazwyać się Command i dziedziczyć po CaseCommand"""

    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        """Miejsce na dodatkowe opcje np. szczególny autor"""
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # if not check_author_dirs():
        #     raise CommandError('Create authors dirs before')

        for sutta in Sutta.objects.all():
            # filename = SUTTA_OUTPUT_FILENAME.format(id=sutta.id)
            filename = SUTTA_OUTPUT_FILENAME.format(sutta_nr=sutta.sutta_nr, author=sutta.author)
            render_sutta(filename, 'sutta.html', sutta)


# zakladamy, ze katolog pl zawsze istnieje (czyli zamiast output mamy pl)


# os.path.exists
# os.mkdir

# https://docs.python.org/3/library/os.html
#
# pl
# author
# collection +
#
# ###
# buildhtmldocs - -->  dokumentacja
#
# .gitignore
