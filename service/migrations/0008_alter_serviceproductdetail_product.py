# Generated by Django 3.2.5 on 2021-08-06 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_productentry_init_stock'),
        ('service', '0007_alter_serviceproductdetail_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceproductdetail',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
    ]