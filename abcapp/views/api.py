from rest_framework import viewsets, routers

from abcapp.models import CampaignMembership


# ViewSets define the view behavior.
class CampaignMembershipViewSet(viewsets.ModelViewSet):
    model = CampaignMembership


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'memberships', CampaignMembershipViewSet)
