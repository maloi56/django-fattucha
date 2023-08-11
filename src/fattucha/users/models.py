from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    SEX_CHOICES = ((None, 'Выберите пол'),
                   (0, 'Мужской'),
                   (1, 'Женский'))
    ACTIVITY_CHOICES = ((None, 'Выберите значение вашей активности'),
                        (1.2, 'Минимальный (сидячий образ жизни)'),
                        (1.375, 'Низкий (редко занимаетесь спортом)'),
                        (1.55, 'Средний (занимаетесь спортом 3-5 раз в неделю)'),
                        (1.725, 'Высокий (интенсивные тренировки 6-7 раз в неделю)'),
                        (1.9, 'Очень высокий (физическая работа и активность)'))

    email = models.EmailField("email", blank=True, unique=True)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    date_birth = models.DateField(null=True, blank=True)
    weight = models.IntegerField(validators=[MaxValueValidator(200), MinValueValidator(0)], null=True, blank=True)
    height = models.IntegerField(validators=[MaxValueValidator(250), MinValueValidator(0)], null=True, blank=True)
    aim = models.IntegerField(validators=[MaxValueValidator(20000), MinValueValidator(0)], null=True, blank=True,
                              default=0)
    sex = models.SmallIntegerField(choices=SEX_CHOICES, null=True, blank=True)
    activity = models.FloatField(choices=ACTIVITY_CHOICES, null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    premium_date = models.DateTimeField(null=True, blank=True)

    def is_liked(self, pk):
        return self.likes.filter(recipe=pk).exists()

    def get_premium(self, tariff_id):
        duration = Tariff.objects.get(pk=tariff_id).duration * 30
        self.premium_date = now() + timedelta(days=duration)
        self.save()

    @property
    def is_premium_active(self):
        return now() < self.premium_date if self.premium_date else False


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateField(auto_now=True)
    expiration = models.DateTimeField()

    def send_verification_email(self):
        link = reverse('users:verify', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username} на портале FatTucha'
        context = {
            'user_email': self.user.email,
            'verification_link': verification_link,
        }

        # Сгенерируйте HTML и текстовую версии сообщения
        html_message = render_to_string('users/confirmation_email.html', context)
        # Отправьте письмо
        email = EmailMultiAlternatives(
            subject=subject,
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.user.email],
        )
        email.content_subtype = 'html'
        email.send()

    def is_expired(self):
        return now() >= self.expiration


class Tariff(models.Model):
    name = models.CharField(max_length=64, default='empty')
    price = models.IntegerField()
    duration = models.IntegerField()

    def __str__(self):
        return f'Тариф \'{self.name}\' за {self.price} рублей'
