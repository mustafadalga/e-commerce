# Generated by Django 2.2.5 on 2019-09-24 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_card'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='brank',
            new_name='brand',
        ),
    ]
