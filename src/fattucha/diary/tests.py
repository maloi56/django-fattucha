import django

django.setup()
import json
from datetime import date
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse, reverse_lazy

from diary.forms import AddProductForm, ChangeModalForm, DiaryForm
from diary.models import DailyReport, FoodInReport, Products, ReportType
from users.models import User


class IndexViewTestCase(TestCase):

    def test_index_get(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'FatTucha')
        self.assertEqual(response.template_name[0], 'diary/index.html')


class DiaryViewTestCase(TestCase):
    # fixtures = ['products.json'] Пока что не работает из-за кодировки

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', email='testuser@yandex.ru', password='qwerasdfzxc1')
        self.path = reverse('diary:diary')
        self.products = Products.objects.all()
        self.diary_obj, self.created = DailyReport.objects.get_or_create(date=date.today(), user=self.user)
        self.tested_product = Products.objects.create(name='окрошка',
                                                      calories=267,
                                                      protein=12,
                                                      fat=15,
                                                      carbohydrates=19)
        self.report_type = ReportType.objects.get(pk=1)
        self.data = {'product': self.tested_product.pk,
                     'weight': 100,
                     'report_type': self.report_type.pk,
                     'report': self.diary_obj.pk
                     }
        self.food = FoodInReport.objects.create(product=self.tested_product,
                                                weight=self.data['weight'],
                                                report=self.diary_obj,
                                                report_type=self.report_type)

    def test_diary_get_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'FatTucha - Дневник')
        self.assertEqual(response.template_name[0], 'diary/diary.html')

        self.assertIsInstance(response.context_data['form'], DiaryForm)
        self.assertIsInstance(response.context_data['change_modal_form'], ChangeModalForm)

        self.assertEqual(response.context_data['products'], json.dumps(list(self.products.values())))
        self.assertEqual(response.context_data['diary_obj'], self.diary_obj)

    def test_diary_get_failure(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f'{reverse("users:login")}?next={self.path}')

    def test_post_add_food_in_diary(self):
        new_data = self.data.copy()
        new_data['weight'] = 555
        self.client.force_login(self.user)
        path = reverse('diary:add_in_diary')

        response = self.client.post(path, new_data)

        self.assertTrue(FoodInReport.objects.filter(report=new_data['report'], weight=555))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('diary:diary'))

    def test_get_add_food_in_diary(self):
        self.client.force_login(self.user)
        path = reverse('diary:add_in_diary')

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('diary:diary'))

    def test_post_change_food_in_diary(self):
        self.assertEqual(self.food.weight, self.data['weight'])
        self.client.force_login(self.user)
        path = reverse_lazy('diary:change_food', args=(self.food.pk,))
        new_data = self.data.copy()
        new_data['weight'] = self.data['weight'] + 150
        new_data['food_id'] = self.food.id

        response = self.client.post(path, new_data)
        self.food.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('diary:diary'))

        self.assertEqual(self.food.weight, self.data['weight'] + 150)

    def test_post_remove_food_from_diary(self):
        self.client.force_login(self.user)
        path = reverse_lazy('diary:remove_food', args=(self.food.pk,))

        response = self.client.get(path)

        self.assertFalse(FoodInReport.objects.filter(pk=self.food.pk).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('diary:diary'))

    def test_get_change_food_in_diary(self):
        self.client.force_login(self.user)
        path = reverse('diary:add_in_diary')

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('diary:diary'))


class AddNewProductViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', email='testuser@yandex.ru', password='qwerasdfzxc1')
        self.data = {'name': 'окрошка',
                     'calories': 267,
                     'protein': 12,
                     'fat': 15,
                     'carbohydrates': 19}
        self.path = reverse('diary:add_product')

    def test_add_new_product_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'FatTucha - Добавление нового продукта')
        self.assertEqual(response.template_name[0], 'diary/add_product.html')
        self.assertIsInstance(response.context_data['form'], AddProductForm)

    def test_add_new_product_failure(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f'{reverse("users:login")}?next={self.path}')

    def test_add_product_post_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('diary:diary'))
        self.assertTrue(Products.objects.filter(name=self.data['name'],
                                                calories=self.data['calories'],
                                                fat=self.data['fat'],
                                                protein=self.data['protein'],
                                                carbohydrates=self.data['carbohydrates']).exists())
