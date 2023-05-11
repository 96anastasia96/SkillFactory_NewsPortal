from datetime import datetime
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.core.mail import mail_admins
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post, Appointment, Category
from .filters import PostFilter
from .forms import PostForm
from django.db.models import Q
from django.contrib import messages
from django.utils.text import slugify


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


#class PostCategoryList(ListView):
#    model = Post
#    template_name = 'news_by_category.html'
#    context_object_name = 'posts'
#    paginate_by = 10


#def news_by_category(request, category):
#    news_items = Post.objects.filter(category=category)  # фильтруем новости по категории
#    context = {
#        'category': category,
#        'news_items': news_items
#    }
#    return render(request, 'news_by_category.html', context)


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


#def subscribe(request):
#    if request.method == 'POST':
#        name = request.POST.get('name', None)
#        email = request.POST.get('email', None)
#        category = request.POST.get('category', None)
#
#        if not email or not name:
#            messages.error(request,
#                           f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
#            return redirect("/")
#
#        if get_user_model().objects.filter(email=email).first():
#            messages.error(request,
#                           f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
#            return redirect(request.META.get("HTTP_REFERER", "/"))
#
#        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
#        if subscribe_user:
#            messages.error(request, f"{email} email address is already subscriber.")
#            return redirect(request.META.get("HTTP_REFERER", "/"))
#
#        try:
#            validate_email(email)
#        except ValidationError as e:
#            messages.error(request, e.messages[0])
#            return redirect("/")
#
#        subscribe_model_instance = SubscribedUsers()
#        subscribe_model_instance.name = name
#        subscribe_model_instance.email = email
#        subscribe_model_instance.category = category
#        subscribe_model_instance.save()
#        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
#        return redirect(request.META.get("HTTP_REFERER", "/"))
#
#
# @user_is_superuser
# def newsletter(request):
#    form = NewsletterForm()
#    form.fields['receiver'].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
#    return render(request=request, template_name='newsletter.html', context={'form': form})


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts})


class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'


class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'category'
