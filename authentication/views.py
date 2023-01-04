from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from authentication.forms import SignUpForm


class UserPageView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('authentication:sign_in')
    template_name = 'user_page.html'

    def get_context_data(self, **kwargs):
        return {"user": self.request.user}


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('authentication:sign_in')


class SignInView(LoginView):
    template_name = 'sign_in.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('authentication:auth_index')
