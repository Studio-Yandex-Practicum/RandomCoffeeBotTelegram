from controlcenter.views import DashboardView

from bot.dashboards import DashPair, Diogramm, MyDashboard, PairDiogramm
from bot.models import ItSpecialist, Profession, Recruiter
from core.forms import DateForm


class DashView(DashboardView):
    """Вью для отображения дашбордов."""

    template_name = "controlcenter/dashboard.html"

    def post(self, request, *args, **kwargs):
        """Запрос для получения статистики в интервале."""
        if request.method == "POST":
            pk = self.kwargs.get("pk")
            form = DateForm(request.POST or None)

            class Diog(Diogramm):
                """Дашборд для переопределения."""

                def values(self):
                    """Переопределение в интервале."""
                    time = form.data.getlist("date")
                    values = []
                    [
                        values.append(
                            (
                                profession.name,
                                ItSpecialist.objects.filter(
                                    profession=profession.pk,
                                    registration_date__range=time,
                                ).count(),
                            )
                        )
                        for profession in Profession.objects.all()
                    ]
                    values.append(
                        (
                            Recruiter._meta.verbose_name,
                            Recruiter.objects.filter(
                                registration_date__range=time
                            ).count(),
                        )
                    )
                    return values

            MyDashboard.widgets = (Diog, DashPair, PairDiogramm)
            self.dashboard = self.dashboards[pk]
            return super(DashboardView, self).get(request, *args, **kwargs)
