import django

django.setup()

import uuid
from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now

from users.forms import UserLoginForm, UserProfileForm, UserRegForm
from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):
    def setUp(self) -> None:
        self.data = {'username': 'tesst',
                     'password1': 'qwerasdfzxc1',
                     'password2': 'qwerasdfzxc1',
                     'email': 'bezt5609@yandex.ru'}
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'FatTucha - Регистрация')
        self.assertEqual(response.template_name[0], 'users/registration.html')
        self.assertIsInstance(response.context_data['form'], UserRegForm)

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.data)

        # check reg logic

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # email verify

        email_verify = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verify.exists())
        self.assertEqual(email_verify.first().expiration.date(),
                         (now() + timedelta(hours=48)).date())

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.')

        User.objects.create(email=self.data['email'])
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким Email уже существует.')


class EmailVerifyViewTestCase(TestCase):
    def setUp(self) -> None:
        self.code = uuid.uuid4()
        self.user = User.objects.create(email='beztfake1@yandex.ru')

    def test_user_email_verify_get_success(self):
        expiration = now() + timedelta(hours=48)
        email_verify = EmailVerification.objects.create(user=self.user, code=self.code, expiration=expiration)
        path = reverse_lazy('users:verify', kwargs={'email': self.user.email, 'code': self.code})

        response = self.client.get(path)
        self.user.refresh_from_db()

        # default asserts
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'FatTucha - Подтверждение электронной почты')
        self.assertEqual(response.context_data['is_success'], True)
        self.assertEqual(response.template_name[0], 'users/email_verification.html')
        # check db changes
        self.assertFalse(EmailVerification.objects.filter(pk=email_verify.pk).exists())
        self.assertEqual(self.user.is_verified_email, True)

    def test_user_email_verify_get_expired(self):
        expiration = now() - timedelta(hours=24)
        email_verify = EmailVerification.objects.create(user=self.user, code=self.code, expiration=expiration)
        path = reverse_lazy('users:verify', kwargs={'email': self.user.email, 'code': self.code})

        response = self.client.get(path)
        self.user.refresh_from_db()

        # default asserts
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'FatTucha - Подтверждение электронной почты')
        self.assertEqual(response.context_data['is_success'], False)
        self.assertEqual(response.template_name[0], 'users/email_verification.html')
        # check db changes
        self.assertFalse(EmailVerification.objects.filter(pk=email_verify.pk).exists())
        self.assertTrue(EmailVerification.objects.filter(user=self.user).exists())
        self.assertEqual(self.user.is_verified_email, False)

    def test_user_email_verify_get_redirect(self):
        path = reverse_lazy('users:verify', kwargs={'email': self.user.email, 'code': self.code})
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))


class LoginViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', email='testuser@yandex.ru', password='qwerasdfzxc1')
        self.path = reverse('users:login')

    def test_user_login_get_success(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'FatTucha - Авторизация')
        self.assertEqual(response.template_name[0], 'users/login.html')
        self.assertIsInstance(response.context_data['form'], UserLoginForm)

    def test_user_login_post_success(self):
        # check username auth
        data = {'username': 'testuser',
                'password': 'qwerasdfzxc1'}

        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

        # check email auth
        data = {'email': 'testuser@yandex.ru',
                'password': 'qwerasdfzxc1'}

        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

    def test_user_login_post_error(self):
        data = {'username': 'wronguser',
                'password': 'wrongpass'}

        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.context_data['form'].errors)


class ProfileViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', email='testuser@yandex.ru', password='qwerasdfzxc1')
        self.path = reverse_lazy('users:profile', args=(self.user.pk,))

    def test_user_profile_get_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'FatTucha - Личный кабинет')
        self.assertEqual(response.template_name[0], 'users/profile.html')
        self.assertIsInstance(response.context_data['form'], UserProfileForm)

    def test_user_profile_get_redirect_to_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('users:profile', args=(99999,)))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.path)

    def test_user_profile_get_redirect_to_login(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f'{reverse("users:login")}?next={self.path}')

    def test_user_profile_post(self):
        data = {'username': self.user.username,
                'email': self.user.email,
                'last_name': "тест"}
        self.client.force_login(self.user)

        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, data['last_name'])
