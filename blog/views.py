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
from rest_framework.parsers import FileUploadParser,MultiPartParser,FormParser
from rest_framework.decorators import action
from rest_framework import filters


class PostApiView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsPostOwnerOrIsAdmin]

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # filter_backends = [filters.SearchFilter]
    # search_filters = ['category',]


    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    

    def create(self,request):
        data = request.data
        data['user'] = request.user.id
        serializer = PostSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=404)

class PostLikeApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        # print(request.data)
        post_id = request.data['post']
        post = get_object_or_404(Post.objects.all(),pk=post_id)
        post.likes.add(user)
        return Response(status=200)

class PostViewsApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        user = request.user
        # print(request.data)
        post_id = request.data['post']
        post = get_object_or_404(Post.objects.all(),pk=post_id)
        post.views.add(user)
        return Response(status=200)

class PostFollowerApiView(APIView):

    def post(self,request):
        user = request.user
        # print(request.data)
        post_id = request.data['post']
        post = get_object_or_404(Post.objects.all(),pk=post_id)
        post.followers.add(user)
        return Response(status=200)



class CommentApiView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsPostOwnerOrCommentOwnerOrIsAdmin]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self,request):
        data = request.data
        data['user'] = request.user.id
        serializer = CommentSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=404)


class ReplyApiView(ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsPostOwnerOrReplyOwnerOrIsAdmin]
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def create(self,request):
        data = request.data
        data['user'] = request.user.id
        serializer = ReplySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=404)
    

class CategoryApiView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class UserApiView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnUserOrIsAdmin]
    parser_classes = [MultiPartParser,FormParser]
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    @action(detail=True, methods=['put'])
    def profile(self,request,pk=None):
        user = self.get_object()
      
        serializer = ProfileSerializer(user.profile,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_serializer = UserSerializer(request.user,many=False)
            return Response(user_serializer.data,status=200)
        else:
            return Response(serializer.errors,status=404)
        

    



class TutorialApiView(ModelViewSet):
    serializer_class = TutorialSerializer
    queryset = Tutorial.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsOwnUserOrIsAdmin]
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
            user_serializer = UserSerializer(user,many=False)
            refresh = RefreshToken.for_user(user)
            resp = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user':user_serializer.data
                }
            return Response(resp,status=200)
        else:
            return Response(serializer.errors,status=404)


class UserRegisterApiView(APIView):
    
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            user_serializer = UserSerializer(user,many=False)
            refresh = RefreshToken.for_user(user)
            resp = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user':user_serializer.data
                }
            return Response(resp,status=200)
        else:
            return Response(serializer.errors,status=404)

class UploadAvatarApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]

    def post(self,request): 
        print(request.FILES)
        serializer = ProfileSerializer(data=request.data,instance=request.user.profile,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_serializer = UserSerializer(request.user,many=False)
            return Response(user_serializer.data,status=200)
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
            
    
