from django.contrib import admin

from django.utils.html import format_html
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin
from .models import *


# @admin.register(User)
admin.AdminSite.site_header=format_html("<h3>Learn More</h3>")



# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ['likes']
    list_display = ['title','user','category','total_likes','total_views','created_at']
    date_hierarchy = 'created_at'

    list_filter = [
        'category',
        
    ]
    search_fields = ['title','user__username']
    @admin.display
    def total_likes(self,obj):
        return len(obj.likes.all())
    @admin.display
    def total_views(self,obj):
        return len(obj.views.all())

    
class ProfileInline(admin.StackedInline):
    model = Profile

class CustomUserAdmin(UserAdmin):
    list_display = ['username','email','full_name','gender','is_active']
    inlines=[ProfileInline]
    list_filter = ['is_superuser','is_staff','is_active','profile__gender',]
    search_fields = ['username','first_name','last_name']


    @admin.display
    def full_name(self,obj):
        return f"{obj.first_name} {obj.last_name}"
    
    @admin.display
    def gender(self,obj):
        return obj.profile.gender
    
    

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user','content','post','created_at']
    search_fields = ['user__username','post__title']
    date_hierarchy = 'created_at'

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    
    list_display = ['id','user','content','comments','created_at','post']
    search_fields = ['user__username','content']
    date_hierarchy = "created_at"

    @admin.display
    def comments(self,obj):
        return obj.comment.content
    
    @admin.display
    def post(self,obj):
        return obj.comment.post.title

admin.site.register(Category)
# admin.site.register(Profile)
# admin.site.register(Comment)
# admin.site.register(Reply)
