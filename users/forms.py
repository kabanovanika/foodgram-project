from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text='First Name', label='Имя пользователя',
                           widget=forms.TextInput(attrs={'class': 'form__input', 'type': 'text'}))
    email = forms.EmailField(max_length=150, help_text='Email', label='Адрес электронной почты',
                             widget=forms.EmailInput(attrs={'class': 'form__input', 'type': 'email'}))
    password1 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': '********', 'class': 'form__input', 'type': 'password',
                                           'data-toggle': 'password'}),
                                label='Пароль',
                                help_text=password_validation.password_validators_help_text_html())
    password2 = None

    class Meta:
        model = User
        exclude = ('last_name',)
        fields = ('username', 'name',
                  'email', 'password1',)
        labels = {
            'username': _('Имя'),
        }


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100, label='Старый пароль',
                                   widget=forms.PasswordInput(attrs={'class': 'form__input', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100, label='Новый пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form__input', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100, label='Подтверждение нового пароля',
                                    widget=forms.PasswordInput(attrs={'class': 'form__input', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class PasswordsResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Адрес электронной почты"), max_length=254)
