import json
import uuid

from datetime import timedelta
from http import HTTPStatus
from fattucha.settings import logger

from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages import error
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory

from calculator.forms import TariffForm
from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegForm
from users.models import EmailVerification, Tariff, User

Configuration.account_id = settings.ACCOUNT_ID
Configuration.secret_key = settings.KASSA_SECRET_KEY


class ProfileView(SuccessMessageMixin, TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    login_url = reverse_lazy('users:login')
    title = 'FatTucha - Личный кабинет'
    success_message = 'Данные успешно обновлены!'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.pk,))

    def get(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.pk:
            return HttpResponseRedirect(reverse_lazy('users:profile', args=(self.request.user.pk,)))
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        error(self.request, form.errors)
        return super().form_invalid(form)


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True
    title = 'FatTucha - Авторизация'


class RegistrationView(SuccessMessageMixin, TitleMixin, CreateView):
    model = User
    form_class = UserRegForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/registration.html'
    success_message = 'Вы успешно зарегистрированы!'
    title = 'FatTucha - Регистрация'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super().get(request, *args, **kwargs)


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'FatTucha - Подтверждение электронной почты'
    is_success = True

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verify = EmailVerification.objects.filter(user=user, code=code)

        if email_verify.exists() and not user.is_verified_email:
            if not email_verify.first().is_expired():
                user.is_verified_email = True
                user.save()
                email_verify.first().delete()
                return super().get(request, *args, **kwargs)
            else:
                email_verify.first().delete()
                expiration = now() + timedelta(hours=48)
                new_email_verify = EmailVerification.objects.create(code=uuid.uuid4(), expiration=expiration, user=user)
                new_email_verify.send_verification_email()
                self.is_success = False
                return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users:login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_success'] = self.is_success
        return context


class PremiumView(TitleMixin, FormView):
    template_name = 'users/premium.html'
    title = 'FatTucha - Премиум'
    form_class = TariffForm
    success_url = reverse_lazy('users:premium')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tariffs'] = Tariff.objects.all().order_by('price')
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        tariff = Tariff.objects.get(pk=request.POST['tariffs'])
        payment = Payment.create({
            "amount": {
                "value": tariff.price,
                "currency": "RUB"
            },
            "metadata": {
                "user_id": self.request.user.pk,
                "tariff_id": tariff.pk
            },
            "confirmation": {
                "type": "redirect",
                "return_url": 'https://fattucha.ru/'
            },
            "capture": True,
            "description": f"Премиум аккаунт {tariff.name} на FatTucha"
        }, uuid.uuid4())
        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)


@logger.catch
@csrf_exempt
def youkassa_webhook_view(request):
    event_json = json.loads(request.body)
    try:
        notification_object = WebhookNotificationFactory().create(event_json)
        logger.info(f'notification_object - {notification_object.object.metadata}')
        response_object = notification_object.object.metadata
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            User.objects.get(pk=int(response_object['user_id'])).get_premium(int(response_object['tariff_id']))
        else:
            return HttpResponse(status=400)
    except Exception:
        return HttpResponse(status=400)

    return HttpResponse(status=200)
