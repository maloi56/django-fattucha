from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.utils.timezone import now

from users.models import User
from users.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите логин или email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-2', 'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ('email', 'password',)


class UserRegForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите email'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя пользователя'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Повторите пароль'
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=True)
        send_email_verification.delay(user.pk)
        return user


class UserProfileForm(UserChangeForm):
    today = now().date()
    delta = today - timedelta(days=14 * 365)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя пользователя', 'readonly': True
    }))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите фамилию'
    }))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control', 'placeholder': 'Выберите файл'
    }))
    email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите email', 'readonly': True
    }))
    date_birth = forms.DateField(required=False,
                                 widget=forms.DateInput(
                                     attrs={
                                         'class': 'form-control',
                                         'onfocus': "(this.type='date')",
                                         'onblur': "(this.type='text') (this.placeholder='дд.мм.гггг')",
                                         'min': datetime.strptime('1930.01.01', '%Y.%m.%d').date(),
                                         'max': delta,
                                     }))

    weight = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите ваш текущий вес'
    }))
    height = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите ваш рост'
    }))
    aim = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите цель по каллориям'
    }))
    sex = forms.TypedChoiceField(empty_value=None, choices=User.SEX_CHOICES, required=False,
                                 widget=forms.Select(attrs={
                                     'class': 'form-select'
                                 }))
    activity = forms.TypedChoiceField(empty_value=None, choices=User.ACTIVITY_CHOICES, required=False,
                                      widget=forms.Select(attrs={
                                          'class': 'form-select'
                                      }))

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'image', 'email', 'date_birth', 'weight', 'height', 'aim',
            'activity', 'sex')
