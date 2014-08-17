from django.test import TestCase
from django.utils import timezone
from time import sleep

from abcapp.models import Campaign
from abcapp.tests.factories import CampaignFactory


class MetadataMixinTextCase(TestCase):

    def test_object_metadata_dates(self):
        # .created
        before_creation = timezone.now()
        campaign = CampaignFactory.create(title=u'Testcampaign')
        campaign.save()
        after_creation = timezone.now()
        self.assertTrue(before_creation < campaign.created < after_creation)

        # .updated
        updated_at_creation = campaign.updated
        campaign.start = timezone.now()  # update the campaign
        campaign.save()
        self.assertTrue(campaign.updated > after_creation)
        self.assertTrue(campaign.updated > updated_at_creation)

        # .deleted
        self.assertEqual(campaign.deleted, None)
        before_delete = timezone.now()
        campaign.delete()
        campaign.save()
        after_delete = timezone.now()
        self.assertTrue(before_delete < campaign.deleted < after_delete)

    def test_object_is_marked_as_deleted(self):
        campaign = CampaignFactory.create(title=u'Testcampaign')
        campaign2 = CampaignFactory.create(title=u'Testcampaign')
        campaign.save()
        campaign2.save()
        self.assertTrue(len(Campaign.objects.all()), 2)

        # when we delete an object and save it, it is removed from objects
        campaign.delete()
        campaign.save()
        self.assertTrue(len(Campaign.objects.all()), 1)

        # but still present in the deleted and with_deleted query sets
        self.assertTrue(len(Campaign.objects.with_deleted_set.all()), 2)
        self.assertTrue(len(Campaign.objects.deleted_set.all()), 1)

    def test_delete_does_not_save_automatically(self):
        campaign = CampaignFactory.create(title=u'Testcampaign')
        campaign.save()
        self.assertEqual(len(Campaign.objects.all()), 1)

        # delete does not save automatically
        campaign.delete()
        self.assertEqual(len(Campaign.objects.all()), 1)
        self.assertEqual(len(Campaign.objects.deleted_set.all()), 0)

        # if we save the object, it is removed from Campaign.objects
        campaign.save()
        self.assertEqual(len(Campaign.objects.all()), 0)
        self.assertEqual(len(Campaign.objects.deleted_set.all()), 1)

    def test_object_is_marked_as_deleted_date(self):
        campaign = CampaignFactory.create(title=u'Testcampaign')
        campaign.save()
        self.assertEqual(campaign.deleted, None)

        before_delete = timezone.now()
        campaign.delete()
        campaign.save()
        after_delete = timezone.now()

        self.assertNotEqual(campaign.deleted, None)
        self.assertTrue(before_delete < campaign.deleted < after_delete)
