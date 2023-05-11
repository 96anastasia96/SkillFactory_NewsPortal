from django.contrib import admin
from .models import Post, Category
    #Profile


class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_date')


admin.site.register(Post)
admin.site.register(Category)
#admin.site.register(SubscribedUsers, SubscribedUsersAdmin)
#admin.site.register(Profile)


