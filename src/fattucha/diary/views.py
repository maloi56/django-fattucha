import json
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import error
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.core.cache import cache
from django.db.models.functions import Length
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from diary.forms import AddProductForm, ChangeModalForm, DiaryForm
from diary.models import DailyReport, FoodInReport, Products


class IndexView(TitleMixin, TemplateView):
    template_name = 'diary/index.html'
    title = 'FatTucha'


class ReportWeekView(TitleMixin, TemplateView):
    template_name = 'diary/reports_week.html'
    title = 'FatTucha - Отчеты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        year = kwargs['year'] if 'year' in kwargs else today.isocalendar()[0]
        week = kwargs['week'] if 'week' in kwargs else today.isocalendar()[1]

        week_objects, total_calories = DailyReport.get_week_objects(user=self.request.user, year=year, week=week)
        context['current_date'] = {'date': today, 'year': date.today().isocalendar()[0], 'week': today.isocalendar()[1]}
        context['week_objects'] = week_objects
        context['calories'] = total_calories
        context['week'] = week
        return context


class ReportView(TitleMixin, TemplateView):
    template_name = 'diary/reports.html'
    title = 'FatTucha - Отчеты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now_date = kwargs['date'] if 'date' in kwargs else date.today()
        diary_obj, created = DailyReport.objects.get_or_create(date=now_date, user=self.request.user)
        context['day'] = now_date
        context['diary_obj'] = diary_obj.get_today()
        context['total_sum'] = context['diary_obj'].total_sum()

        context['current_date'] = {'date': date.today(), 'year': date.today().isocalendar()[0],
                                   'week': date.today().isocalendar()[1]}
        return context


class DairyView(TitleMixin, LoginRequiredMixin, TemplateView):
    template_name = 'diary/diary.html'
    title = 'FatTucha - Дневник'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now_date = self.request.GET['date'] if 'date' in self.request.GET else date.today()

        context['form'] = DiaryForm()
        context['change_modal_form'] = ChangeModalForm()

        diary_obj, created = DailyReport.objects.get_or_create(date=now_date, user=self.request.user)

        context['day'] = diary_obj
        context['diary_obj'] = diary_obj.get_today()
        context['total_sum'] = context['diary_obj'].total_sum()
        return context


class AddInDiaryView(LoginRequiredMixin, CreateView):
    model = FoodInReport
    form_class = DiaryForm
    template_name = 'diary/diary.html'
    success_url = reverse_lazy('diary:diary')
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('diary:diary'))

    def form_valid(self, form):
        response = super().form_valid(form)

        # Обновление кэша
        if not settings.DEBUG:  # Temporary solution
            cache_key = f'week_objects:{self.request.user.pk}:' \
                        f'{self.object.report.date.year}:' \
                        f'{self.object.report.date.isocalendar()[1]}'
            cache.delete(cache_key)

        return response

    def form_invalid(self, form):
        error(self.request, form.errors)
        return HttpResponseRedirect(reverse('diary:diary'))


class ChangeFoodView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = FoodInReport
    form_class = ChangeModalForm
    template_name = 'diary/diary.html'
    login_url = reverse_lazy('users:login')
    success_url = reverse_lazy('diary:diary')
    success_message = 'Данные успешно обновлены'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('diary:diary'))

    def form_invalid(self, form):
        error(self.request, form.errors)
        return HttpResponseRedirect(reverse('diary:diary'))


@login_required
def remove_food(request, food_id):
    instance = FoodInReport.objects.filter(pk=food_id, report__user__id=request.user.pk).first()
    if instance is not None:
        instance.delete()
        messages.success(request, 'Запись удалена!')
        cache_key = f'week_objects:{request.user.pk}:{instance.report.date.year}:{instance.report.date.isocalendar()[1]}'
        cache.delete(cache_key)
    return HttpResponseRedirect(reverse('diary:diary'))


@login_required
def get_products(request):
    search = request.GET.get('q')
    if search:
        vector = SearchVector('name', 'brand')
        query = SearchQuery(search, )
        result = Products.objects.annotate(rank=SearchRank(vector, query, cover_density=True)).filter(
            rank__gte=0.0001).order_by('-rank', Length('name').asc())
        return JsonResponse({'products': list(result.values())})
    else:
        return JsonResponse({'products': None})


class AddProductView(TitleMixin, LoginRequiredMixin, CreateView):
    model = Products
    form_class = AddProductForm
    success_url = reverse_lazy('diary:diary')
    template_name = 'diary/add_product.html'
    login_url = reverse_lazy('users:login')
    title = 'FatTucha - Добавление нового продукта'

    def form_invalid(self, form):
        error(self.request, form.errors)
        return HttpResponseRedirect(reverse('diary:diary'))
