from django.contrib import admin
from .models import Post, Category, PostCategory
from modeltranslation.admin import TranslationAdmin
from .translation import Post, Category


class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_date')


# создаём новый класс для представления товаров в админке
#class PostAdmin(admin.ModelAdmin):
#    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
#    list_display = ('title', 'text', 'time_in') # оставляем только имя и цену товара
#    list_filter = ('title', 'text', 'time_in')  # добавляем примитивные фильтры в нашу админку
#    search_fields = ('title', 'category__name')  # тут всё очень похоже на фильтры из запросов в базу


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)







