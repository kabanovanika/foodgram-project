from django.urls import path
from . import views

urlpatterns = [
    path("password-change/", views.PasswordsChangeView.as_view(template_name='changePassword.html'),
         name="change_password"),
    path("password-reset/", views.PasswordResetView.as_view(template_name='resetPassword.html'),
         name='reset_password'),
    path("password-reset/done/", views.reset_success, name='password_reset_done'),
    path("password-success/", views.password_success, name='password_success'),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("login/", views.view_login, name="login"),
    path("logout/", views.logout_view, name='logout')
]
