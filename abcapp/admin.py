from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.db.models import get_app
from django.db.models import get_models

# Our models are regitered directly in abcapp.models.


def unregister_django_phpBB3():
    models = get_models(get_app('django_phpBB3'))
    for model in models:
        try:
            admin.site.unregister(model)
        except NotRegistered:
            print 'not registered'

unregister_django_phpBB3()
