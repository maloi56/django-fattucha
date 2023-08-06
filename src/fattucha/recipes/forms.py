from django import forms

from diary.models import Products

from .models import CookingSteps, Ingredient, Recipe, RecipeCategory


class RecipeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите название рецепта'}), label='Название', required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Введите описание рецепта'}), label='Описание')
    portion = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите количество порций', 'type': 'number', 'min': 1}),
        label='Количество порций')
    time_to_cook = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Минуты', 'type': 'number', 'min': 0}), label='Время приготовления')
    category = forms.ModelChoiceField(empty_label='Выберите категорию', queryset=RecipeCategory.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-select'}), label='Категория')
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control', 'placeholder': 'Выберите файл', 'id': 'image-input', 'style': 'display : None'}),
        label='Фотография готового блюда')

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'portion', 'time_to_cook', 'category', 'image',)


class IngredientForm(forms.ModelForm):
    product = forms.ModelChoiceField(empty_label='Выберите ингредиент', queryset=Products.objects.all(),
                                     widget=forms.TextInput(attrs={'class': 'form-select'}), label='Ингредиент')
    weight = forms.FloatField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите вес', 'type': 'number', 'min': 1}),
        label='Вес г')

    class Meta:
        model = Ingredient
        fields = ('product', 'weight',)


class StepsForm(forms.ModelForm):
    step = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control mt-3', 'type': 'hidden', 'min': 1, 'readonly': True, 'value': 1}))
    how_to_cook = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control mt-3', 'placeholder': 'Введите инструкцию...', 'type': 'number', 'min': 1}))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control', 'placeholder': 'Выберите файл', 'style': 'display : None'}), required=False)

    class Meta:
        model = Ingredient
        fields = ('step', 'how_to_cook', 'image',)


IngredientFormSet = forms.inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=0,
    can_delete=True,
)

CookingStepsFormSet = forms.inlineformset_factory(
    Recipe,
    CookingSteps,
    form=StepsForm,
    extra=1,
    can_delete=True,
)
