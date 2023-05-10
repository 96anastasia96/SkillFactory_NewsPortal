from django.contrib import admin
from .models import Post, Category, PostCategory, SubscribedUsers


class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_date')


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(SubscribedUsers, SubscribedUsersAdmin)


