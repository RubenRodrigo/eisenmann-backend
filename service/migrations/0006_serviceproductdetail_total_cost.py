# Generated by Django 3.2.5 on 2021-08-04 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_serviceproductdetail_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceproductdetail',
            name='total_cost',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
