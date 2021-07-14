from django.contrib import admin

from django.utils.html import format_html

# Register your models here.
from .models import *

admin.AdminSite.site_header=format_html("<h3>Learn More</h3>")
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ['likes']
    list_display = ['title','user','category','total_likes','total_views','created_at']
    @admin.display
    def total_likes(self,obj):
        return len(obj.likes.all())
    @admin.display
    def total_views(self,obj):
        return len(obj.views.all())
    
    

# admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Reply)
