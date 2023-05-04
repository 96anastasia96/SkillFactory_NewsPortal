import django_filters
from django.forms import DateInput, CheckboxSelectMultiple
from django_filters import FilterSet
from .models import Post, Category
from django import forms


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    title = django_filters.Filter(field_name='title', lookup_expr='icontains')
    time_in = django_filters.DateFilter(field_name='time_in', lookup_expr='gte', widget=DateInput(attrs={'type': 'date'}))
    categories = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'categories': 'categories'}), label = 'Categories')

    class Meta:
        model = Post
        fields = {
            # поиск по названию
            'title': ['icontains'],
            'rating': [
                'lt',  # рейтинг должен быть меньше или равен указанному
                'gt',  # рейтинг должен быть больше или равен указанному
            ],
        }
