from django import forms

from bot.models import Recruiter, Student


class StudentForm(forms.ModelForm):
    """Форма для модели IT-специалиста в админ-панели."""

    class Meta:
        model = Student
        fields = "__all__"

    def clean_telegram_id(self):
        """Проверка, есть ли рекрутер с таким же id."""
        telegram_id = self.cleaned_data.get("telegram_id")
        if Recruiter.objects.filter(telegram_id=telegram_id).exists():
            raise forms.ValidationError("Рекрутер с таким ID уже есть в базе")


class RecruiterForm(forms.ModelForm):
    """Форма для модели рекрутера в админ-панели."""

    class Meta:
        model = Recruiter
        fields = "__all__"

    def clean_telegram_id(self):
        """Проверка, есть ли IT-специалист с таким же id."""
        telegram_id = self.cleaned_data.get("telegram_id")
        if Student.objects.filter(telegram_id=telegram_id).exists():
            raise forms.ValidationError(
                "IT-специалист с таким ID уже есть в базе"
            )
