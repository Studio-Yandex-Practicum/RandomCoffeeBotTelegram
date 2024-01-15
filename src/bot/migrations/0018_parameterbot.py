# Generated by Django 4.2.7 on 2024-01-12 19:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0017_alter_messagebot_message"),
    ]

    operations = [
        migrations.CreateModel(
            name="ParameterBot",
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
                (
                    "title",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        verbose_name="Название параметра бота",
                    ),
                ),
                (
                    "value",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Значение параметра бота",
                    ),
                ),
                (
                    "unit_measurement",
                    models.CharField(
                        max_length=50, verbose_name="Единица измерения параметра бота"
                    ),
                ),
                (
                    "parameter_key",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[A-z0-9_]+$",
                                code="Invalid key",
                                message="Ключ должен стостоять только из латинских букв, цифр и знака подчеркивания",
                            )
                        ],
                        verbose_name="Ключ параметра бота",
                    ),
                ),
            ],
            options={
                "verbose_name": "Параметр бота",
                "verbose_name_plural": "Параметры бота",
            },
        ),
    ]