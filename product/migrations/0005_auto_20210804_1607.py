# Generated by Django 3.2.5 on 2021-08-04 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20210804_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='subproduct',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]