# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0006_division_commander'),
        ('django_phpBB3', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='phpbb_user',
            field=models.ForeignKey(to='django_phpBB3.User', to_field='id'),
            preserve_default=True,
        ),
    ]
