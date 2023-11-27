from controlcenter import Dashboard, widgets

from bot.models import (
    CreatedPair,
    ItSpecialist,
    PassedPair,
    Profession,
    Recruiter,
)


class Diogramm(widgets.SinglePieChart):
    """Диаграмма IT-специалистов разных профессий."""

    title = "Статистика IT-специалистов разных профессий."
    width = 6

    def legend(self):
        """Легенда создания диаграммы."""
        return self.series

    def values(self):
        """Значения передаваемые в диаграмму."""
        values = []

        [
            values.append(
                (
                    profession.name,
                    ItSpecialist.objects.filter(
                        profession=profession.pk
                    ).count(),
                )
            )
            for profession in Profession.objects.all()
        ]
        values.append(
            (Recruiter._meta.verbose_name, Recruiter.objects.count())
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

    def values(self):
        """Значения передаваемые в диаграмму."""
        return [
            (
                "Общее количество пар",
                CreatedPair.objects.count() + PassedPair.objects.count(),
            )
        ]


class DashPair(widgets.SingleBarChart):
    """Таблица пар."""

    title = "Статистика пар."
    width = 3

    def legend(self):
        """Легенда создания таблицы."""
        return self.series

    def values(self):
        """Значения передаваемые в таблицу."""
        titles = ["Незавершенные пары", "Завершенные пары"]
        values = []
        [
            values.append((titles[index], model.objects.count()))
            for index, model in enumerate((CreatedPair, PassedPair))
        ]
        return values


class MyDashboard(Dashboard):
    """Вывод всех таблиц."""

    widgets = (
        Diogramm,
        DashPair,
        PairDiogramm,
    )
