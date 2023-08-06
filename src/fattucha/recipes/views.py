from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import error, success
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from common.views import TitleMixin
from recipes.forms import CookingStepsFormSet, IngredientFormSet, RecipeForm
from recipes.models import Likes, Recipe, RecipeCategory
from recipes.paginator import MyPaginator


class RecipesViews(TitleMixin, ListView):
    template_name = 'recipes/recipes.html'
    title = 'FatTucha - Рецепты'
    model = Recipe
    context_object_name = 'recipes'
    paginator_class = MyPaginator
    paginate_by = 6
    delta_first = 0

    def get_queryset(self):
        queryset = super().get_queryset().filter(status=Recipe.APPROVED)
        search = self.request.GET.get('q')
        if search:
            vector = SearchVector('name', )
            query = SearchQuery(search, )
            result = self.model.objects.annotate(rank=SearchRank(vector, query, cover_density=True)).filter(
                rank__gte=0.0001).order_by('-rank')
            return result
        else:
            filter = self.kwargs.get('filter')
            category_id = self.kwargs.get('category_id')
            result = queryset.filter(category_id=category_id) if category_id \
                else queryset
            return result.order_by('pk') if filter == 'all' else result.filter(creator=self.request.user.id).order_by(
                'pk')

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs):
        if self.delta_first:
            kwargs['delta_first'] = self.delta_first
        return super().get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs)

    def get(self, request, *args, **kwargs):
        if kwargs.get('filter') is None or kwargs.get('filter') == 'my' and not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('recipes:recipes', kwargs={'filter': 'all', 'page': 1}))
        if kwargs.get('filter') == 'my' and kwargs.get('page'):
            self.delta_first = 1
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = RecipeCategory.objects.all().order_by('name')
        context['q_arg'] = self.request.GET.get('q', 'None')
        return context


class AddRecipeView(LoginRequiredMixin, TitleMixin, TemplateView):
    title = 'FatTucha - Добавить рецепт'
    template_name = 'recipes/add_recipe.html'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RecipeForm()
        context['steps_formset'] = CookingStepsFormSet()
        context['ingredient_formset'] = IngredientFormSet(queryset=Recipe.objects.none())
        return context

    def post(self, *args, **kwargs):
        recipe_form = RecipeForm(self.request.POST, self.request.FILES)
        ingredient_formset = IngredientFormSet(self.request.POST)
        steps_formset = CookingStepsFormSet(self.request.POST, self.request.FILES)
        if recipe_form.is_valid() and ingredient_formset.is_valid() and steps_formset.is_valid():
            recipe_form.instance.creator = self.request.user
            recipe = recipe_form.save()
            for form in ingredient_formset:
                ingredient = form.save(commit=False)
                ingredient.recipe = recipe
                ingredient.save()
            for form in steps_formset:
                step = form.save(commit=False)
                step.recipe = recipe
                step.save()
            success(request=self.request, message='Ваш рецепт отправлен на рассмотрение, спасибо за ваш вклад!')
            return HttpResponseRedirect(reverse('recipes:recipes'))
        else:
            error(self.request, recipe_form.errors)
            error(self.request, ingredient_formset.errors)
            error(self.request, steps_formset.errors)
            return self.get(*args, **kwargs)


class RecipeInstanceView(TitleMixin, DetailView):
    title = 'FatTucha - Добавить рецепт'
    model = Recipe
    template_name = 'recipes/recipe_instance.html'
    pk_url_kwarg = 'recipe_id'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portion_info'] = kwargs['object'].get_portion_info()
        context['liked'] = self.request.user.is_liked(kwargs['object'])
        return context

    def get_queryset(self):
        return super().get_queryset().filter(status=Recipe.APPROVED)


@login_required
def like_post(request):
    recipe_id = int(request.POST.get('recipe_id'))
    user = request.user
    recipe = Recipe.objects.get(pk=recipe_id)
    if not user.is_liked(pk=recipe):
        Likes.objects.create(recipe=recipe, user=user)
    else:
        Likes.objects.filter(recipe=recipe, user=user).delete()
    return JsonResponse({'likes': Likes.objects.filter(recipe=recipe).get_sum_likes()})
