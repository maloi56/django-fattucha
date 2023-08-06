from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.timezone import now

from users.models import Tariff, User


class UserCalcForm(UserChangeForm):
    today = now().date()
    delta = today - timedelta(days=14 * 365)
    date_birth = forms.DateField(required=False,
                                 widget=forms.DateInput(
                                     attrs={
                                         'class': 'form-control',
                                         'onfocus': "(this.type='date')",
                                         'onblur': "(this.type='text') (this.placeholder='дд.мм.гггг')",
                                         'min': datetime.strptime('1930.01.01', '%Y.%m.%d').date(),
                                         'max': delta,
                                     }))

    weight = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите ваш текущий вес'
    }))
    height = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите ваш рост'
    }))
    aim = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите цель по каллориям'
    }))
    sex = forms.TypedChoiceField(empty_value=None, choices=User.SEX_CHOICES,
                                 widget=forms.Select(attrs={
                                     'class': 'form-select'
                                 }))
    activity = forms.TypedChoiceField(empty_value=None, choices=User.ACTIVITY_CHOICES,
                                      widget=forms.Select(attrs={
                                          'class': 'form-select'
                                      }))

    class Meta:
        model = User
        fields = ('date_birth', 'weight', 'height', 'aim', 'sex', 'activity')


class TariffForm(forms.ModelForm):
    tariffs = forms.ModelChoiceField(empty_label="Выберите тариф", queryset=Tariff.objects.all().order_by('price'),
                                     initial=None,
                                     widget=forms.Select(attrs={
                                         'class': 'form-select'
                                     }))

    class Meta:
        model = Tariff
        fields = ('id',)
