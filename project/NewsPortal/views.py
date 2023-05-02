from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwards):
        context = super().get_context_data(**kwards)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'some_news.html'
    context_object_name = 'some_news'
