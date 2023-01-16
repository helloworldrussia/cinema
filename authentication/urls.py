from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import path, reverse_lazy

from .views import SignInView, SignUpView

app_name = 'authentication'
urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('sign-in/', SignInView.as_view(), name='sign_in'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('authentication:sign_in')), name='logout'),
    path('password-change/',
         PasswordChangeView.as_view(
             success_url=reverse_lazy('movies:movie_list'),
             template_name='password_change.html'
         ),
         name='password_change'
         ),
]
