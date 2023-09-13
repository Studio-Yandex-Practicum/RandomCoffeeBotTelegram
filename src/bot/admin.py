from django.contrib import admin

from .models import CreatedPair, PassedPair, Recruter, Student


@admin.register(CreatedPair)
class CreatedPairAdmin(admin.ModelAdmin):
    """Управление созданной парой."""


@admin.register(PassedPair)
class PassedPairAdmin(admin.ModelAdmin):
    """Управление моделью созвона."""


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Управление моделью студента."""


@admin.register(Recruter)
class RecruterAdmin(admin.ModelAdmin):
    """Управление моделью рекрутера."""
