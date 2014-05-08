from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.db.models import get_app
from django.db.models import get_models

from abcapp.models import Campaign
from abcapp.models import CampaignParticipation
from abcapp.models import Army
from abcapp.models import Division
from abcapp.models import Rank
from abcapp.models import Medal
from abcapp.models import Player


# Unregister all django_phpBB3 models cause we don't want to edit
# phpBB-Data from Django.

def unregister_django_phpBB3():
    models = get_models(get_app('django_phpBB3'))
    for model in models:
        try:
            admin.site.unregister(model)
        except NotRegistered:
            print 'not registered'

unregister_django_phpBB3()


#
# Register our models with some customizations
#

def registerModels():
    '''will be called at the end of this file after we have defined
    the custom model admins.
    '''
    admin.site.register(Campaign)
    admin.site.register(Army)
    admin.site.register(Division)
    admin.site.register(Rank)
    admin.site.register(Medal)
    admin.site.register(Player, PlayerAdmin)


class CampaignParticipationInline(admin.StackedInline):

    model = Player.campaigns.through
    extra = 0
    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

    #     field = super(CampaignParticipationInline,
    #                   self).formfield_for_foreignkey(db_field, request,
    #                                                  **kwargs)

    #     if db_field.name == 'inside_room':
    #         if request._obj_ is not None:
    #             field.queryset = field.queryset.filter(
    #                 building__exact=request._obj_)
    #         else:
    #             field.queryset = field.queryset.none()

    #     return field


class PlayerAdmin(admin.ModelAdmin):

    inlines = (CampaignParticipationInline,)
    readonly_fields = ('phpbb_user', 'django_user')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(PlayerAdmin, self).get_form(request, obj, **kwargs)


registerModels()
