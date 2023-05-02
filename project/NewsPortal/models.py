from django.contrib.auth.models import User
from django.db import models


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
    name_category = models.CharField(max_length=40, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TYPE, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
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


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


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
