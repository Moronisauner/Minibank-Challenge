# Generated by Django 2.0 on 2017-12-30 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0003_auto_20171228_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
