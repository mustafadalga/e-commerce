# Generated by Django 2.2.5 on 2019-09-23 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20190914_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='customer_id',
            field=models.BooleanField(blank=True, max_length=120, null=True),
        ),
    ]
