from django.urls import path
from . import views

urlpatterns = [
    path("password-change/", views.PasswordsChangeView.as_view(template_name='changePassword.html'),
         name="change_password"),
    path("password-success/", views.password_success, name='password_success'),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.view_login, name="login"),
]
