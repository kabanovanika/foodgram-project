from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CreationForm, SignUpForm
from django.contrib.auth import authenticate, login


def view_login(request):
    print(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print('ятут')
        if user is not None:
            print('ятут1')
            login(request, user)
            return redirect('/')
        else:
            print('ятут2')
            return redirect('/signup')
    return render(request, 'authForm.html')


# class Login(CreateView):
#     form_class = CreationForm
#     success_url = reverse_lazy("login")
#     template_name = "authForm.html"


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
