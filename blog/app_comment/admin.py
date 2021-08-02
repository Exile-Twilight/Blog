from django.contrib import admin
from .models import Comment
from blog.base_admin import BaseOwnerAdmin
from blog.custom_site import custom_site


# Register your models here.

@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ['target', 'nickname', 'content', 'website', 'created_time']
