# Generated by Django 4.2.5 on 2023-09-29 11:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0002_recruiter_search_start_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recruiter",
            name="surname",
            field=models.CharField(
                max_length=255, null=True, verbose_name="Фамилия"
            ),
        ),
        migrations.AlterField(
            model_name="itspecialist",
            name="surname",
            field=models.CharField(
                max_length=255, null=True, verbose_name="Фамилия"
            ),
        ),
    ]
