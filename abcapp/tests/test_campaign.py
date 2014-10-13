from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from abcapp.models import Campaign
from abcapp.tests.factories import CampaignFactory


class CampaignTestCase(TestCase):

    @classmethod
    def _create_campaign(cls, title, start=None, end=None):
        kwargs = {'title': title}
        if start:
            kwargs['start'] = start
        if end:
            kwargs['end'] = end
        return CampaignFactory.create(**kwargs)

    def test_capaign_created(self):
        self._create_campaign(u'Testcampaign')
        campaigns = Campaign.objects.all()
        self.assertEqual(len(campaigns), 1)
        self.assertEqual(campaigns[0].title, u'Testcampaign')

    def test_current_campaigns(self):
        now = timezone.now()
        self._create_campaign(u'Campaign in the past',
                              start=(now - timedelta(days=20)),
                              end=(now - timedelta(days=10)))
        self._create_campaign(u'Campaign started, not yet ended',
                              start=now - timedelta(days=5),
                              end=None)
        # campaign not started yet
        self._create_campaign(u'Campaign not yet started',
                              start=now + timedelta(days=20),
                              end=None)
        current_campaigns = Campaign.current_campaigns()
        self.assertEqual(len(current_campaigns), 1)
        self.assertEqual(current_campaigns[0].title,
                         u'Campaign started, not yet ended')

    def test_upcoming_campaigns(self):
        now = timezone.now()
        self._create_campaign(u'Campaign in the past',
                              start=(now - timedelta(days=20)),
                              end=(now - timedelta(days=10)))
        self._create_campaign(u'Campaign started, not yet ended',
                              start=now - timedelta(days=5),
                              end=None)
        # campaign not started yet
        self._create_campaign(u'Campaign not yet started',
                              start=now + timedelta(days=20),
                              end=None)
        current_campaigns = Campaign.upcoming_campaigns()
        self.assertEqual(len(current_campaigns), 1)
        self.assertEqual(current_campaigns[0].title,
                         u'Campaign not yet started')

    def test_past_campaigns(self):
        now = timezone.now()
        self._create_campaign(u'Campaign in the past',
                              start=(now - timedelta(days=20)),
                              end=(now - timedelta(days=10)))
        self._create_campaign(u'Campaign started, not yet ended',
                              start=now - timedelta(days=5),
                              end=None)
        # campaign not started yet
        self._create_campaign(u'Campaign not yet started',
                              start=now + timedelta(days=20),
                              end=None)
        current_campaigns = Campaign.past_campaigns()
        self.assertEqual(len(current_campaigns), 1)
        self.assertEqual(current_campaigns[0].title,
                         u'Campaign in the past')

    def test_campaign_finished(self):
        now = timezone.now()
        campaign = self._create_campaign(u'Testcampaign',
                                         start=(now - timedelta(days=20)),
                                         end=None)

        self.assertEqual(campaign.finished, False)
        campaign.end = now - timedelta(days=1)
        self.assertEqual(campaign.finished, True)

    def test_campaign_started(self):
        now = timezone.now()
        campaign = self._create_campaign(u'Testcampaign',
                                         start=(now - timedelta(days=20)),
                                         end=None)

        self.assertEqual(campaign.started, True)

        campaign = self._create_campaign(u'Testcampaign',
                                         start=(now + timedelta(days=20)),
                                         end=None)
        self.assertEqual(campaign.started, False)

    def test_campaign_running(self):
        now = timezone.now()
        campaign = self._create_campaign(u'Past Testcampaign',
                                         start=(now - timedelta(days=20)),
                                         end=(now - timedelta(days=10)))

        self.assertEqual(campaign.running, False)

        campaign = self._create_campaign(u'Running Testcampaign 1',
                                         start=(now - timedelta(days=20)),
                                         end=(now + timedelta(days=10)))

        self.assertEqual(campaign.running, True)

        campaign = self._create_campaign(u'Running Testcampaign 2',
                                         start=(now - timedelta(days=20)),
                                         end=None)

        self.assertEqual(campaign.running, True)

        campaign = self._create_campaign(u'Future Testcampaign',
                                         start=(now + timedelta(days=20)),
                                         end=None)

        self.assertEqual(campaign.running, False)
