# Generated by Django 3.2.5 on 2021-08-19 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20210817_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productstock',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_stock', to='product.product'),
        ),
    ]
