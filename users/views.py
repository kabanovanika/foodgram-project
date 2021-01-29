from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy
from .forms import SignUpForm, PasswordChangingForm, PasswordsResetForm
from django.contrib.auth import authenticate, login, logout



def logout_view(request):
    logout(request)
    return render(request, 'logout_success.html')


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


class PasswordsResetView(PasswordResetView):
    form_class = PasswordsResetForm
    success_url = reverse_lazy('reset_success')


def password_success(request):
    return render(request, 'password_success.html')


def reset_success(request):
    return render(request, 'password_reset_done.html')


def view_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')

    return render(request, 'authForm.html')


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'reg.html'


