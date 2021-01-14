from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import CreationForm, SignUpForm


# class SignUp(CreateView):
#     form_class = CreationForm
#     success_url = reverse_lazy("login")
#     template_name = "reg.html"
#
#
class Login(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "authForm.html"


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
