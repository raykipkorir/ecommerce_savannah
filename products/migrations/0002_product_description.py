# Generated by Django 5.0.2 on 2024-02-15 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="description",
            field=models.CharField(default="This is a description", max_length=200),
            preserve_default=False,
        ),
    ]
