# Generated by Django 2.2.5 on 2019-09-23 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_billingprofile_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingprofile',
            name='customer_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
