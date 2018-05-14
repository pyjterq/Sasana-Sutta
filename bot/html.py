import json
from django.template.loader import render_to_string


def render_sutta(filename, template, sutta):
    content = render_to_string(template, {
        'title': sutta.title,
        'title_pali': sutta.title_pali,
        'phapragraph_list': json.loads(sutta.content),
        'author': sutta.author,
        'collection': sutta.collection,
        'sutta_nr': sutta.sutta_nr,
    })

    with open(filename, mode='w') as doc:
        doc.write(content)
