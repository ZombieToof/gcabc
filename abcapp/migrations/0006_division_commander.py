# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_phpBB3', '__first__'),
        ('abcapp', '0005_army_general'),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='commander',
            field=models.ForeignKey(to_field='id', blank=True, to='django_phpBB3.User', null=True),
            preserve_default=True,
        ),
    ]
