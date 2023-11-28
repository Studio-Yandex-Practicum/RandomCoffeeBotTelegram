from datetime import timedelta

from controlcenter import Dashboard, widgets
from django.utils import timezone

from bot.models import (
    CreatedPair,
    ItSpecialist,
    PassedPair,
    Profession,
    Recruiter,
)

INTERVAL_DATA = 10
INTERVAL_DASHBOARDS = (timezone.now() - timedelta(1), timezone.now())


class Diogramm(widgets.SinglePieChart):
    """Диаграмма IT-специалистов разных профессий."""

    title = "Статистика IT-специалистов разных профессий."
    width = 6

    def legend(self):
        """Легенда создания диаграммы."""
        return self.series

    @property
    def get_form_time(self, time=INTERVAL_DASHBOARDS):
        """Переопределение промежутка во времени статистики."""
        return time

    def values(self):
        """Значения передаваемые в диаграмму."""
        values = []

        [
            values.append(
                (
                    profession.name,
                    ItSpecialist.objects.filter(
                        profession=profession.pk,
                        registration_date__range=self.get_form_time,
                    ).count(),
                )
            )
            for profession in Profession.objects.all()
        ]
        values.append(
            (
                Recruiter._meta.verbose_name,
                Recruiter.objects.filter(
                    registration_date__range=self.get_form_time
                ).count(),
            )
        )
        return values


class PairDiogramm(widgets.SinglePieChart):
    """Диаграмма показывающая количество пар."""

    title = "Общее количество пар."
    width = 3
    CONTROLCENTER_CHARTIST_COLORS = "default"

    def legend(self):
        """Легенда создания диаграммы."""
        return self.series

    @property
    def get_form_time(self, time=INTERVAL_DASHBOARDS):
        """Переопределение промежутка во времени статистики."""
        return time

    def values(self):
        """Значения передаваемые в диаграмму."""
        return [
            (
                "Общее количество пар",
                CreatedPair.objects.filter(
                    itspecialist__registration_date__range=self.get_form_time
                ).count()
                + PassedPair.objects.filter(
                    itspecialist__registration_date__range=self.get_form_time
                ).count(),
            )
        ]


class DashPair(widgets.SingleBarChart):
    """Таблица пар."""

    title = "Статистика пар."
    width = 3

    def legend(self):
        """Легенда создания таблицы."""
        return self.series

    @property
    def get_form_time(self, time=INTERVAL_DASHBOARDS):
        """Переопределение промежутка во времени статистики."""
        return time

    def values(self):
        """Значения передаваемые в таблицу."""
        titles = ["Незавершенные пары", "Завершенные пары"]
        values = []
        [
            values.append(
                (
                    titles[index],
                    model.objects.filter(
                        itspecialist__registration_date__range=self.get_form_time
                    ).count(),
                )
            )
            for index, model in enumerate((CreatedPair, PassedPair))
        ]
        return values


class InervalWidget:
    """Промежуточный виджет."""

    def __init__(self, form):
        """Получение времени."""
        self.time = form.data.getlist("date")

    def widgets(self):
        """Добавление интервала для статистики."""
        for model in (Diogramm, PairDiogramm, DashPair):
            model.get_form_time = self.time


class MyDashboard(Dashboard):
    """Вывод всех таблиц."""

    widgets = (
        Diogramm,
        DashPair,
        PairDiogramm,
    )
