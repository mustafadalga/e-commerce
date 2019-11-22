# Generated by Django 2.2.5 on 2019-10-16 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_product_is_digital'),
        ('billing', '0010_auto_20190927_0904'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0006_auto_20191015_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPurchaseManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPurchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('retunded', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]