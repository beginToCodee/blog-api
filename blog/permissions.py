from rest_framework.permissions import BasePermission
from rest_framework import permissions
from .models import *

class IsPostOwnerOrIsAdmin(BasePermission):
    def has_object_permission(self,request,view,obj):
        print(permissions.SAFE_METHODS)
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        return request.user == obj.user
    
class IsPostOwnerOrCommentOwnerOrIsAdmin(BasePermission):
    def has_object_permission(self,request,view,obj):
        post = Post.objects.filter(pk=obj.post.id).first()
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser or request.user==post.user:
            return True
        return request.user == obj.user



class IsPostOwnerOrReplyOwnerOrIsAdmin(BasePermission):
    def has_object_permission(self,request,view,obj):
        post = Post.objects.filter(pk=obj.post.id).first()
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser or request.user==post.user:
            return True
        return request.user == obj.user

class IsOwnUserOrIsAdmin(BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        return request.user == obj