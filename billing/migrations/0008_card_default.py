# Generated by Django 2.2.5 on 2019-09-24 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_auto_20190924_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='default',
            field=models.BooleanField(default=True),
        ),
    ]
