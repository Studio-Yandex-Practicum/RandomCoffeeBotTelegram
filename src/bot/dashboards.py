from controlcenter import Dashboard, widgets

from bot.models import CreatedPair, PassedPair, Recruiter, Student


class RecruiterItemList(widgets.ItemList):
    """Список рекрутеров."""

    model = Recruiter
    list_display = (
        "name",
        "telegram_username",
        "registration_date",
        "search_start_time",
    )
    title = "Статистика рекрутеров."
    width = 10
    height = 1000


class StudentItemList(widgets.ItemList):
    """Список студентов."""

    model = Student
    list_display = (
        "name",
        "telegram_username",
        "registration_date",
        "search_start_time",
    )
    title = "Статистика студентов."
    width = 10


class CreatedPairItemList(widgets.ItemList):
    """Список созданных пар."""

    model = CreatedPair
    list_display = ("student", "recruiter")
    title = "Статистика созданных пар."
    width = 10


class PassedPairItemList(widgets.ItemList):
    """Список созвонившихся пар."""

    model = PassedPair
    list_display = ("student", "recruiter")
    title = "Статистика созвонившихся пар."
    width = 10


class Diogramm(widgets.SinglePieChart):
    """Диаграмма студентов, рекрутеров, пар."""

    title = "Статистика рекрутеров, студентов и пар."
    width = 3

    def legend(self):
        """Легенда создания диаграммы."""
        return self.series

    def values(self):
        """Значения передаваемые в диаграмму."""
        values = []
        [
            values.append((model._meta.verbose_name, model.objects.count()))
            for model in (Student, Recruiter, CreatedPair, PassedPair)
        ]
        return values


class DashPair(widgets.SingleBarChart):
    """Таблица пар."""

    title = "Статистика пар."
    width = 3

    def legend(self):
        """Легенда создания таблицы."""
        return self.series

    def values(self):
        """Значения передаваемые в таблицу."""
        values = []
        [
            values.append((model._meta.verbose_name, model.objects.count()))
            for model in (CreatedPair, PassedPair)
        ]
        return values


class MyDashboard(Dashboard):
    """Вывод всех таблиц."""

    widgets = (
        DashPair,
        Diogramm,
        (
            RecruiterItemList,
            StudentItemList,
            CreatedPairItemList,
            PassedPairItemList,
        ),
    )
