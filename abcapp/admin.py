from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from abcapp.models import Campaign
from abcapp.models import Army
from abcapp.models import Division
from abcapp.models import Rank
from abcapp.models import Medal
from abcapp.models import Player


# Unregister all django_phpBB3 models cause we don't want to edit
# phpBB-Data from Django.

def unregister_django_phpBB3():
    app_config = apps.get_app_config('django_phpBB3')
    models = app_config.get_models()
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
    admin.site.register(Division, DivisionAdmin)
    admin.site.register(Rank)
    admin.site.register(Medal)
    admin.site.register(Player, PlayerAdmin)


class CampaignMembershipInline(admin.StackedInline):

    model = Player.campaigns.through
    extra = 0
    readonly_fields = ('campaign',)
    fields = (('campaign', 'army', 'division'),
              ('ranks', 'medals'),
              'notes')

    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

    #     field = super(CampaignMembershipInline,
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

    inlines = (CampaignMembershipInline,)
    readonly_fields = ('phpbb_user', 'django_user')
    list_display = ('colored_name',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(PlayerAdmin, self).get_form(request, obj, **kwargs)


class DivisionAdmin(admin.ModelAdmin):

    list_display = ('title', 'army', 'campaign')

    def campaign(self, obj):
        return obj.army.campaign

    campaign.admin_order_field = 'army__campaign'

registerModels()
