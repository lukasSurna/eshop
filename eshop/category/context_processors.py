from . import models

def menu_links(request):
    links = models.Category.objects.all()
    return dict(links=links)