from django.urls import path
from .views import (PostList, PostDetailView, PostCreate, PostUpdate, PostDelete, SearchResultsView, ArticleDelete,
                    ArticleUpdate, ArticleCreate, ArticleDetailView, byebye, AppointmentView, CategoryView,
                    AddCategoryView, CategoryList)

urlpatterns = [
    path('posts/', PostList.as_view(), name ='post_list'),
    path('news/<int:pk>/', PostDetailView.as_view(), name='some_news'),
    path('news/create/', PostCreate.as_view(), name='new_post'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('article/create/', ArticleCreate.as_view(), name='new_article'),
    path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('byebye/', byebye, name='byebye'),
#path('news_by_category/', PostCategoryList.as_view(), name='news_by_category'),
    path('appointment_created/', AppointmentView.as_view(), name='appointment_created'),
    path('make_appointment/', AppointmentView.as_view(), name='make_appointment'),
#path('subscribe/', subscribe, name='subscribe'),
#path('news_by_category/<int:pk>/', PostCategoryList.as_view(), name='category-detail'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('category_list/', CategoryList.as_view(), name='category_list'),

]