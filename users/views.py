from django.shortcuts import render, redirect
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
    return render(request, 'reset_success.html')


def view_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            return redirect('/auth/signup')
    return render(request, 'authForm.html')


def signup_view(request):
    form = SignUpForm(request.POST)
    print('валидна?')
    print(form.errors)
    if form.is_valid():
        print('валидна')
        user = form.save()
        user.refresh_from_db()
        print(form.cleaned_data)
        user.name = form.cleaned_data.get('name')
        user.email = form.cleaned_data.get('email')
        user.save()
        print(user.name)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        name = form.cleaned_data.get('name')
        user = authenticate(username=username, password=password, name=name)
        login(request, user)
        return redirect('/home')
    else:
        form = SignUpForm()
    return render(request, 'reg.html', {'form': form})
