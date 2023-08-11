from django import forms

from diary.models import DailyReport, FoodInReport, Products


class AddProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите название продукта'
    }), label='Название продукта')
    brand = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите марку продукта'
    }), label='Марка (бренд)')
    calories = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите калории'
    }), label='Калории (на 100 грамм)')
    protein = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите белки'
    }), label='Белки (на 100 грамм)')
    fat = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите жиры'
    }), label='Жиры (на 100 грамм)')
    carbohydrates = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите углеводы'
    }), label='Углеводы (на 100 грамм)')

    class Meta:
        model = Products
        fields = ('brand', 'name', 'calories', 'protein', 'fat', 'carbohydrates', )


class DiaryForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Products.objects.all(),
                                     widget=forms.TextInput(attrs={'id': 'product_id', 'type': 'hidden'}))
    report_type = forms.IntegerField(widget=forms.TextInput(attrs={'id': "report_type", 'type': 'hidden'}))
    weight = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите вес продукта', 'id': "food-weight", 'type': 'number'}))
    report = forms.ModelChoiceField(queryset=DailyReport.objects.all(),
                                    widget=forms.TextInput(attrs={'id': "report", 'type': 'hidden'}))

    class Meta:
        model = FoodInReport
        fields = ('product', 'weight', 'report_type', 'report')


class ChangeModalForm(forms.ModelForm):
    food_id = forms.ModelChoiceField(queryset=FoodInReport.objects.all(),
                                     widget=forms.TextInput(attrs={'id': 'food_id'}))
    product = forms.ModelChoiceField(queryset=Products.objects.all(),
                                     widget=forms.TextInput(attrs={'id': 'change_product_id'}))
    report_type = forms.IntegerField(widget=forms.TextInput(attrs={'id': "change_report_type"}))
    weight = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите вес продукта', 'id': "change_food_weight", 'type': 'number'}))

    class Meta:
        model = FoodInReport
        fields = ('product', 'weight', 'report_type',)
