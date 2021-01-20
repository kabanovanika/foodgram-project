from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy
from .forms import SignUpForm, PasswordChangingForm, PasswordsResetForm
from django.contrib.auth import authenticate, login


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
    print(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/auth/signup')
    return render(request, 'authForm.html')


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.name = form.cleaned_data.get('name')
        user.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'reg.html', {'form': form})
