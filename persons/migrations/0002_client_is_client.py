# Generated by Django 4.2.1 on 2023-07-12 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("persons", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="is_client",
            field=models.BooleanField(default=False),
        ),
    ]