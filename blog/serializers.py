from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password,make_password



class ReplySerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()

        

    def get_user_detail(self,obj):
        user = User.objects.get(id=obj.user.id)
        serializer = UserSerializer(user,many=False)
        return serializer.data
    
    class Meta:
        model = Reply
        fields = ['id','content','created_at','comment','user','user_detail']
        read_only_fields = ['id','user_detail']


    

    

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()
    
    def get_replies(self,obj):
        replies = Reply.objects.filter(comment=obj)
        return len(replies)

    def get_user_detail(self,obj):
        user = User.objects.get(id=obj.user.id)
        serializer = UserSerializer(user,many=False)
        return serializer.data
   
    class Meta:
        model = Comment
        fields = ['id','content','created_at','post','user','user_detail','replies']
        read_only_fields = ["id",'user_detail','replies']
    
    
    




class PostSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(read_only=True,many=True)
    comments=serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()

    # def get_user(self,obj):
        
    def get_comments(self,obj):
        comments = Comment.objects.filter(post=obj)
        return len(comments)
    def get_user_detail(self,obj):
        user = User.objects.get(id=obj.user.id)
        serializer = UserSerializer(user,many=False)
        return serializer.data

    class Meta:
        model = Post
        fields = ['id','title','description','thumbnail','category','user','user_detail','comments','likes','views','created_at','updated_at']
        read_only_fields = ['id','user_detail','comments','created_at','updated_at','likes','views']
    
    
    

class TutorialSerializer(serializers.ModelSerializer):
    posts = PostSerializer(read_only=True,many=True)
    class Meta:
        model = Tutorial
        fields = "__all__"
        read_only_fields = ['id']



class CategorySerializer(serializers.ModelSerializer):
    # posts = PostSerializer(read_only=True,many=True)
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['id','user']
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True,many=False)
    # tutorials = TutorialSerializer(read_only=True,many=True)
    # posts = PostSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields=['id','username','email','first_name','last_name','last_login','profile']
        read_only_fields = ['id','password','username']
        ordering = ['id']
  



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,validated_data):
        
        username = validated_data.get('username','')
        password = validated_data.get('password','')
       
        if username and password:
            try:
                user = User.objects.get(username=username)
            except Exception as e:
                print(e)
                errors = {
                    'username':['this username is does not exist']
                }
                raise serializers.ValidationError(errors)
            if check_password(password,user.password):
                validated_data['user']=user
                return validated_data
            else:
                errors = {
                    'password':['password is does not matched']
                }
                raise serializers.ValidationError(errors)
            
        else:
            errors = {
                'username':["this field is required"],
                'password':['this field is required']
            }
            raise serializers.ValidationError(errors)


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    re_password = serializers.CharField()

    def validate(self,validated_data):
        username = validated_data.get('username','')
        email = validated_data.get('email','')
        password = validated_data.get('password','')
        re_password = validated_data.get('re_password','')

        if username and password and email and re_password:
            if User.objects.filter(username=username).first() is None:
                if password != re_password:
                    errors = {
                        're_password':["both password is not matched"]
                    }
                elif password.isdigit():
                    errors = {
                        'password':['only numeric values are not allowed']
                    }
                elif len(password)<8:
                    errors = {
                        'password':['at least 8 charecters are required']
                    }
                else:
                    user = User(username=username,email=email,password=make_password(password))
                    user.save()
                    validated_data['user'] = user
                    return validated_data
            else:
                errors = {
                    'username':['this username is alredy exist']
                }
                
        else:
            errors = {
                'username':['this field is required'],
                'email':['this field is required'],
                'password':['this field is required'],
                're_password':['this field is required']
            }
        raise serializers.ValidationError(errors)