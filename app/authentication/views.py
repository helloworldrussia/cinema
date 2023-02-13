from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from authentication.forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('authentication:sign_in')


class SignInView(LoginView):
    template_name = 'sign_in.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('movies:movie_list')
