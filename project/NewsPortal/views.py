from datetime import datetime
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post, Appointment, Category, Subscription, CategorySubscribe
from .filters import PostFilter
from .forms import PostForm
from django.db.models import Q


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
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
    template_name = 'some_news.html'
    context_object_name = 'some_news'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'new_post.html'
    permission_required = ('NewsPortal.add_post',)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success_url = reverse_lazy('new_post', kwargs={'pk': self.object.id})
        return response


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('some_news')
    permission_required = ('NewsPortal.change_post',)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
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
    template_name = 'article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'new_article.html'
    permission_required = ('NewsPortal.add_post',)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success_url = reverse_lazy('new_article', kwargs={'pk': self.object.id})
        return response


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    success_url = reverse_lazy('new_article')
    permission_required = ('NewsPortal.change_post',)


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('posts')


@login_required(login_url='/accounts/login/')
def byebye(request):
    logout(request)
    return redirect('logout')


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        return redirect('make_appointment')


#def CategoryView(request, cats):
#    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
#    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts})

class CategoryPost(DetailView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'postcategory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category=kwargs['object'])
        return context



class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'


class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'category'


#class CategorySubscribed(View):
#    model = User
#    context_object_name = 'subscribe'
#
#
#    def get_subscribed(self, request):
#        user = request.user
#        if not Category.objects.filter(subscribe=user).exists():
#            Category.subscribe.add(request.user)
#        return redirect('category_subscribe')
#
#    def post(self, request):
#        self.get_subscribed(request)
#        print()
#        return super().post(request)
#

def subscribe_to_category(request, pk):

    current_user = request.user
    CategorySubscribe.objects.create(category=Category.objects.get(pk=pk), subscriber=User.objects.get(pk=current_user.id))

    return render(request, 'subscribe.html')

