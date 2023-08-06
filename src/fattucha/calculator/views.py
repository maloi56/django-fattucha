from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from calculator.forms import UserCalcForm
from common.views import TitleMixin
from users.models import User


class CalculatorView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserCalcForm
    template_name = 'calculator/calculator.html'
    title = 'FatTucha - Калькулятор'
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse_lazy('calculator:calculator', args=(self.request.user.pk,))

    def get(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.pk:
            return HttpResponseRedirect(reverse_lazy('calculator:calculator', args=(self.request.user.pk,)))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = self.request.user
            age = datetime.now().date() - user.date_birth
            if user.sex == 0:
                context['formula'] = (88.36 +
                                      (13.4 * user.weight) +
                                      (4.8 * user.height) -
                                      (5.7 * age.days/365.25)) * user.activity
            elif user.sex == 1:
                context['formula'] = (447.593 +
                                      (9.247 * user.weight) +
                                      (3.098 * user.height) -
                                      (4.330 * age.days / 365.25)) * user.activity
        except Exception:
            pass
        return context
