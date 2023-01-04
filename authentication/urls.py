from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import path, reverse_lazy

from .views import SignInView, SignUpView, UserPageView

app_name = 'authentication'

auth_index_url = reverse_lazy('authentication:auth_index')

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('sign-in/', SignInView.as_view(), name='sign_in'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('authentication:sign_in')), name='logout'),
    path('password-change/',
         PasswordChangeView.as_view(success_url=auth_index_url,
                                    template_name='password_change.html'
                                    ),
         name='password_change'
         ),
    path('', UserPageView.as_view(), name='auth_index'),
]
