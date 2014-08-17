from django.test import TestCase

from abcapp.models import Campaign
from abcapp.tests.factories import CampaignFactory


class CampaignTestCase(TestCase):

    def _create_campaign(self, title):
        return CampaignFactory.create(title=title)

    def test_capaign_created(self):
        self._create_campaign(u'Testcampaign')
        campaigns = Campaign.objects.all()
        self.assertEqual(len(campaigns), 1)
        self.assertEqual(campaigns[0].title, u'Testcampaign')
