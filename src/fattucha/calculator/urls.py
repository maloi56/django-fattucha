from django.urls import path

from calculator.views import CalculatorView

app_name = 'calculator'

urlpatterns = [
    path('<int:pk>/', CalculatorView.as_view(), name='calculator'),
]
