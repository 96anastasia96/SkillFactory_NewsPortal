from datetime import datetime

import username as username
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import mail_admins, send_mail, mail_managers, EmailMultiAlternatives
from django.db.models.signals import post_save
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post, Appointment, Category, CategorySubscribe
from .filters import PostFilter
from .forms import PostForm
from django.db.models import Q


#def notify_new_post_in_category(objects, action):
#    if action == 'post_add':
#        subscriber = []
#        for category_subscribe in CategorySubscribe.objects.filter(category__in=objects.categories.all()):
#            subscriber.append(category_subscribe.subscriber.email)
#
#        send_mail(
#            subject='Здравствуй. Новая статья в твоём любимом разделе!',
#            html_message=render_to_string('new_post.html',
#                                          context={'post': objects,
#                                               'link': f'http://127.0.0.1:8000/news/{objects.id}'}),
#
#
#            message="Hello",
#            recipient_list=subscriber,
#        )
#
#        return redirect('new_post')


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    @method_decorator(login_required)
    def posts(request):
        posts = Post.objects.filter(author=request.user).order_by('-time_in')
        context = {'posts': posts}
        return render(request, 'NewsPortal/posts.html', context)

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwards):
        context = super().get_context_data(**kwards)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        context['filterset'] = self.filterset
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/some_news.html'
    context_object_name = 'some_news'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'posts/new_post.html'
    permission_required = ('NewsPortal.add_post',)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success_url = reverse_lazy('new_post', kwargs={'pk': self.object.id})
        post = self.object
        post_url = self.request.build_absolute_uri(reverse('some_news', args=[post.pk]))
        subscribed_users = self.object.category.get_subscribers()

        send_mail(
            subject=f'Здравствуй. Новая статья в твоём любимом разделе "{post.category}"',
            message=f'{post.text[:20]}...\n\n Ссылка на новый пост: {post_url}',
            from_email='su8scriber@yandex.ru',
            recipient_list=(['su8scriber1@gmail.com'], [user.email for user in subscribed_users]),
        )
        return response



class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'posts/post_edit.html'
    success_url = reverse_lazy('some_news')
    permission_required = ('NewsPortal.change_post',)


class PostDelete(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('post_list')


class SearchResultsView(ListView):
    model = Post
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('Category')
        object_list = Post.objects.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(time_in__icontains=query) |
            Q(rating__icontains=query) |
            Q(type__icontains=query)
        )
        if category_id:
            object_list = object_list.filter(category__id=category_id)
        object_list = object_list.distinct()
        return object_list


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'articles/article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles/new_article.html'
    permission_required = ('NewsPortal.add_post',)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success_url = reverse_lazy('new_article', kwargs={'pk': self.object.id})
        return response


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles/article_edit.html'
    success_url = reverse_lazy('new_article')
    permission_required = ('NewsPortal.change_post',)


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('posts')


@login_required(login_url='/accounts/login/')
def byebye(request):
    logout(request)
    return redirect('logout')


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'appointment/make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        html_content = render_to_string(
            'appointment/appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email='su8scriber@yandex.ru',
            to=['su8scriber1@gmail.com'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "appointment/appointment_created.html")  # добавляем html

        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        msg.send()

        return redirect('make_appointment')


def notify_managers_appointment(sender, instance, created, **kwargs):
    subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )


# коннектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию
post_save.connect(notify_managers_appointment, sender=Appointment)


class CategoryPost(DetailView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'postcategory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category=kwargs['object'])
        return context


class AddCategoryView(CreateView):
    model = Category
    template_name = 'categories/add_category.html'
    fields = '__all__'


class CategoryList(ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'category'


def subscribe_to_category(request, pk):

    current_user = request.user
    CategorySubscribe.objects.create(category=Category.objects.get(pk=pk), subscriber=User.objects.get(pk=current_user.id))

    return render(request, 'subscribe.html')

