from django.urls import path
from .views import (PostList, PostDetailView, PostCreate, PostUpdate, PostDelete, SearchResultsView, ArticleDelete,
                    ArticleUpdate, ArticleCreate, ArticleDetailView, byebye, AppointmentView, CategoryPost,
                    AddCategoryView, CategoryList, subscribe_to_category, posts_created_last_week, Index)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts_created_last_week/', posts_created_last_week, name='posts_created_last_week'),
    path('news/<int:pk>/', cache_page(60*5)(PostDetailView.as_view()), name='some_news'),
    path('news/create/', PostCreate.as_view(), name='new_post'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('article/<int:pk>/', cache_page(60*5) (ArticleDetailView.as_view()), name='article'),
    path('article/create/', ArticleCreate.as_view(), name='new_article'),
    path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('byebye/', byebye, name='byebye'),
    path('appointment_created/', AppointmentView.as_view(), name='appointment_created'),
    path('make_appointment/', AppointmentView.as_view(), name='make_appointment'),
    path('category/<int:pk>/', CategoryPost.as_view(), name='category'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('category_list/', CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/subscribe', subscribe_to_category),
    path('index/', Index.as_view()),
]