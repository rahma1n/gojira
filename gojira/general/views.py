from gojira.utils.views import TemplateView


__author__ = 'nadimrahman'


class HomeView(TemplateView):

    login_required = False
    template_name = "home.html"

home_view = HomeView.as_view()

