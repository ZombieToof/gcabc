# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_phpBB3', '__first__'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE phpbb_users MODIFY user_id integer(8) unsigned NOT NULL AUTO_INCREMENT;'
            ),
        migrations.RunSQL(
            sql='ALTER TABLE phpbb_ranks MODIFY rank_id integer(8) unsigned NOT NULL AUTO_INCREMENT;'
            ),
        migrations.RunSQL(
            sql='ALTER TABLE phpbb_groups MODIFY group_id integer(8) unsigned NOT NULL AUTO_INCREMENT;'
            ),
        migrations.RunSQL(
            sql='ALTER TABLE phpbb_forums MODIFY forum_id integer(8) unsigned NOT NULL AUTO_INCREMENT;'
            ),
        migrations.RunSQL(
            sql='ALTER TABLE phpbb_topics MODIFY topic_id integer(8) unsigned NOT NULL AUTO_INCREMENT;'
            ),
    ]
