# Generated by Django 4.2.3 on 2023-08-05 19:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0007_rename_citem_supplieritems_sitem"),
    ]

    operations = [
        migrations.CreateModel(
            name="Orders",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("item", models.TextField(max_length=40)),
                ("description", models.TextField(max_length=300)),
                (
                    "quantity",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "purchasePrice",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0.01)]
                    ),
                ),
            ],
        ),
    ]
