# Generated by Django 5.0.2 on 2024-02-17 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Acknowledged", "Acknowledged"),
                    ("Cancelled", "Cancelled"),
                    ("Shipped", "Shipped"),
                    ("Delivered", "Delivered"),
                ],
                max_length=20,
            ),
        ),
    ]
