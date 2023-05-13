from datetime import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

article = 'AR'
news = 'NW'

TYPE = [
    (article, "Статья"),
    (news, "Новость")
]


class Author(models.Model):
    name = models.CharField(max_length=255)
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        comment_rating = Comment.objects.filter(user_id=self.users.id).aggregate(models.Sum('rating'))['rating__sum']
        posts_rating = Post.objects.filter(author_id=self).aggregate(models.Sum('rating'))
        post_id = Post.objects.filter(author_id=self).values_list('id', flat=True)
        rating_comment_to_posts = Comment.objects.filter(post_id__in=post_id).aggregate(models.Sum('rating'))[
            'rating__sum']
        self.user_rating = (int(posts_rating['rating__sum']) * 3) + int(comment_rating) + int(rating_comment_to_posts)
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    subscribe = models.ManyToManyField(User,
                                       related_name="subscribed_by",
                                       symmetrical=False,
                                       blank=True)

    def __str__(self):
        return f'{self.name.title()}'

    def get_absolute_url(self):
        return reverse('add_category')


class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    type = models.CharField(max_length=7, choices=TYPE)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=255, default='music')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        text = self.text[:124]
        if len(self.text) > 124:
            text += '...'
        return text

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        if self.type == article:
            return reverse('article', args=[str(self.id)])
        elif self.type == news:
            return reverse('some_news', args=[str(self.id)])
        else:
            return reverse('/', args=[str(self.id)])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class Subscription(models.Model):
    email = models.EmailField(User.email, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


