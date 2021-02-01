from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='Имя')
    username = forms.CharField(max_length=100,
                               help_text='Имя для входа в систему',
                               label='Имя пользователя')
    email = forms.EmailField(max_length=150, label='Адрес электронной почты')
    password1 = forms.CharField(max_length=100,
                                label='Пароль',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': '********',
                                           'class': 'form__input',
                                           'type': 'password',
                                           'data-toggle': 'password'}),
                                help_text='Ваш пароль должен содержать '
                                          'не менее 8 символов.'
                                          'Ваш пароль не должен совпадать с '
                                          'логином.')
    password2 = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email')
        exclude = (
            'last_name',
            'password2',
        )


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=100,
        label='Старый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form__input',
            'type': 'password'
        }))
    new_password1 = forms.CharField(
        max_length=100,
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form__input',
            'type': 'password'
        }))
    new_password2 = forms.CharField(
        max_length=100,
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form__input',
            'type': 'password'
        }))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class PasswordsResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Адрес электронной почты"),
                             max_length=254)
