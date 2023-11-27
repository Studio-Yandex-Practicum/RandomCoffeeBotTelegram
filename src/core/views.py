from controlcenter.views import DashboardView

from bot.dashoboard_widgets import InervalWidget
from core.forms import DateForm


class DashView(DashboardView):
    """Вью для отображения дашбордов."""

    template_name = "controlcenter/dashboard.html"

    def post(self, request, *args, **kwargs):
        """Запрос для получения статистики в интервале."""
        if request.method == "POST":
            pk = self.kwargs.get("pk")
            form = DateForm(request.POST or None)
            InervalWidget(form=form).widgets()
            self.dashboard = self.dashboards[pk]
            return super(DashboardView, self).get(request, *args, **kwargs)
