# coding=utf-8
import logging

from django.conf import settings as gsett
from django.http import HttpResponseForbidden
from django.views import generic

logger = logging.getLogger(__name__)


class DirectTemplateView(generic.TemplateView):
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.extra_context is not None:
            for key, value in self.extra_context.items():
                if callable(value):
                    context[key] = value()
                else:
                    context[key] = value
        return context


def direct_template(template_name):
    return DirectTemplateView.as_view(template_name=template_name)


class TemplateView(generic.TemplateView):
    """
    Provides:
        * set login_required = True for login-required pages, that redirect
            to login page that will return if not logged-in
        * .context dict used to render template_name in context
    """
    login_required = False
    staff_only = False
    require_feature_access = None

    def __init__(self, *args, **kwargs):
        super(TemplateView, self).__init__(*args, **kwargs)
        self.context = {}

    def dispatch(self, request, *args, **kwargs):
        self.login_required = any([self.login_required,
                                   self.staff_only])

        if self.login_required and not request.user.is_authenticated():
            return self.redirect_to_login(request)

        if self.staff_only and not request.user.is_staff:
            return HttpResponseForbidden('Staff only!')

        is_premium = request.session.get('premium')
        self.context['premium'] = is_premium

        return super(TemplateView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def redirect_to_login(cls, request, path=None):
        """
        Adapted out of django's user_passes_test function which is used by the
        login_required decorator.

        Will redirect from request back to login with ?next= set, if logical,
        so that the user comes straight back to where they are
        """
        import urlparse
        from django.contrib.auth import REDIRECT_FIELD_NAME
        from django.contrib.auth.views import redirect_to_login

        if path is None:
            path = request.build_absolute_uri()
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse.urlparse(gsett.LOGIN_URL)[:2]
            current_scheme, current_netloc = urlparse.urlparse(path)[:2]
            if (
                        (not login_scheme or login_scheme == current_scheme)
                    and (not login_netloc or login_netloc == current_netloc)
            ):
                path = request.get_full_path()

        return redirect_to_login(path, None, REDIRECT_FIELD_NAME)

    def get_context_data(self):
        return self.context


class Redirect(TemplateView):
    """
    Base class for views that do nothing but redirect to another place.
    """
    template_name = ''

    def get(self, request):
        raise NotImplementedError()


class BadRequest(Exception):
    pass


class Forbidden(Exception):
    pass
