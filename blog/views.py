
# from typing_extensions import Required
from django.db.models.base import Model
from django.http.response import Http404
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from .permissions import *
from rest_framework.parsers import FileUploadParser,MultiPartParser,FormParser,JSONParser
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import parser_classes
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size=5
    page_size_query_param = 'records'
    max_page_size = 20

class PostApiView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsPostOwnerOrIsAdmin]

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = [JSONParser,MultiPartParser,FormParser]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['category','tutorial']
    search_fields = ['title', 'description','user__username']

    pagination_class = MyPageNumberPagination

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


    def get_serializer(self,*args,**kwargs):
        kwarg_list = list(kwargs.keys())
        
        
        if kwargs.keys() and 'many' not in kwarg_list:
            # kwargs['data']._mutable = True
            if self.request.method == 'POST':
                try:
                    kwargs['data']['user'] = self.request.user.id
                except Exception as e:
                    print(e)
                    kwargs['data']._mutable = True
                    kwargs['data']['user'] = self.request.user.id
            else:
                obj = self.get_object()
                
                kwargs['data']['user'] = obj.user.id
        return super(PostApiView,self).get_serializer(*args,**kwargs)

    @action(detail=True, methods=['put','get'])
    def likes(self,request,pk=None):
        post = get_object_or_404(Post.objects.all(),pk=pk)
        if request.method == 'PUT':
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                return Response(status=204)
            else:
                post.likes.add(request.user)
                return Response(status=200)
        elif request.method == 'GET':
            users = post.likes.all()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data)
        
    
    @action(detail=True, methods=['put','get'])
    def views(self,request,pk=None):

        post = get_object_or_404(Post.objects.all(),pk=pk)

        if request.method == 'PUT':
            post.views.add(request.user)
            return Response(status=200)
        elif request.method == 'GET':
            users = post.views.all()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data)
    
    
    
    @action(detail=True,methods=['get'])
    def comments(self,request,pk=None):
        post = get_object_or_404(Post.objects.all(),pk=pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data,status=200)

        

class CommentApiView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsPostOwnerOrCommentOwnerOrIsAdmin]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['post','user__username']
    pagination_class = MyPageNumberPagination
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer(self,*args,**kwargs):
        kwarg_list = list(kwargs.keys())
        if kwargs.keys() and 'many' not in kwarg_list:
            # kwargs['data']._mutable = True
            if self.request.method == 'POST':
                try:
                    kwargs['data']['user'] = self.request.user.id
                except Exception as e:
                    print(e)
                    kwargs['data']._mutable = True
                    kwargs['data']['user'] = self.request.user.id
            else:
                obj = self.get_object()
                kwargs['data']['user'] = obj.user.id
        return super(CommentApiView,self).get_serializer(*args,**kwargs)
    
    @action(detail=True,methods=['get'])
    def replies(self,request,pk=None):
        comment = get_object_or_404(Comment.objects.all(),pk=pk)
        replies = Reply.objects.filter(comment=comment)
        serializer = ReplySerializer(replies,many=True)
        return Response(serializer.data)
    


    

class ReplyApiView(ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsPostOwnerOrReplyOwnerOrIsAdmin]
    pagination_class = MyPageNumberPagination
    def get_object(self):
        
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_serializer(self,*args,**kwargs):
        kwarg_list = list(kwargs.keys())
        if kwargs.keys() and 'many' not in kwarg_list:
            # kwargs['data']._mutable = True
            if self.request.method == 'POST':
                try:
                    kwargs['data']['user'] = self.request.user.id
                except Exception as e:
                    print(e)
                    kwargs['data']._mutable = True
                    kwargs['data']['user'] = self.request.user.id
                
            else:
                obj = self.get_object()
                kwargs['data']['user'] = obj.user.id
        return super(ReplyApiView,self).get_serializer(*args,**kwargs)
    

class CategoryApiView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsAdminOrReadOnly]

class UserApiView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnUserOrIsAdmin]
    pagination_class = MyPageNumberPagination

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    @action(detail=True, methods=['put'])
    @parser_classes([MultiPartParser,FormParser])
    def profile(self,request,pk=None):
        user = self.get_object()
      
        serializer = ProfileSerializer(user.profile,data=request.data,partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(serializer.data)
            user = get_object_or_404(User.objects.all(),pk=serializer.data['user'])
            user_serializer = UserSerializer(user,many=False)
            return Response(user_serializer.data,status=200)
        else:
            return Response(serializer.errors,status=404)
    
    @action(detail=True, methods=['put','get'])
    def followers(self,request,pk=None):
        user = get_object_or_404(User.objects.all(),pk=pk)
        if request.method == 'PUT':
            if request.user in user.profile.follower.all():
                user.profile.follower.remove(request.user)
                return Response(status=204)
            else:
                user.profile.follower.add(request.user)
                return Response(status=200)
        elif request.method == 'GET':
            users = user.profile.follower.all()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data)

        

    
class TutorialApiView(ModelViewSet):
    serializer_class = TutorialSerializer
    queryset = Tutorial.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsOwnUserOrIsAdmin]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['user']
    search_fields=['name']
    pagination_class = MyPageNumberPagination
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self,request):
        tutorials = Tutorial.objects.filter(user=request.user)
        serializer = TutorialSerializer(tutorials,many=True)
        return Response(serializer.data,status=200)





class UserLoginApiView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            resp = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user':{
                        'id':user.id,
                        'username':user.username
                    }
                }
            return Response(resp,status=200)
        else:
            return Response(serializer.errors,status=404)


class UserRegisterApiView(APIView):
    
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            
            refresh = RefreshToken.for_user(user)
        
            resp = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user':{
                        'id':user.id,
                        'username':user.username
                    }
                }
            return Response(resp,status=200)
        else:
            return Response(serializer.errors,status=404)


class UserLogoutApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        refresh = request.data.get('refresh')
        if refresh:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(status=200)
        else:
            resp = {
                "refresh":["this field is required"]
            }
            return Response(resp,status=404)
            
    
