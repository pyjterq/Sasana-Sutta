from django.db import models
from django.utils import timezone

# Tabelka:
#     url =
#     title =
#     author =
#     content = [
#         {type: 'p', text: ''},
#         {type: 'h1', text: ''},
#         {type: 'p', text: ''},
#         {type: 'h1', text: ''},
#         {type: 'p', text: ''},
#         {type: 'h1', text: ''},
#         {type: 'p', text: ''},
#         {type: 'h1', text: ''},
#         {type: 'p', text: ''},
#         {type: 'h1', text: ''},
#         {type: 'p', text: ''},
#         {type: 'h1', text: ''},
#     ]
#     created_at


class Sutta(models.Model):
    title = models.CharField(max_length=250)
    title_pali = models.CharField(max_length=250)
    url = models.URLField()
    author = models.CharField(max_length=50)
    collection = models.CharField(max_length=250)
    sutta_nr = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            # not self.id oznacza, że obiekt nie nigdy nie był zapisany
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)
