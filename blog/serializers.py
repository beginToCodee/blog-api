from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password,make_password



class ReplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

        

    def get_user(self,obj):
        user = User.objects.get(id=obj.user.id)
        serializer = UserSerializer(user,many=False)
        return serializer.data
    
    class Meta:
        model = Reply
        fields = "__all__"
        read_only_fields = ['id','user','comment']
    
    def save(self,user):
        validated_data = self.validated_data
        validated_data['user']=user
        
        reply = Reply.objects.create(**validated_data)
        return reply
    

class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(read_only=True,many=True)
    user = serializers.SerializerMethodField()

    # def get_user(self,obj):
        

    def get_user(self,obj):
        user = User.objects.get(id=obj.user.id)
        serializer = UserSerializer(user,many=False)
        return serializer.data
   
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["id","user"]
    
    def save(self,user):
        validated_data = self.validated_data
        validated_data['user']=user
        
        comment = Comment.objects.create(**validated_data)
        return comment




class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True,many=True)
    user = serializers.SerializerMethodField()

    # def get_user(self,obj):
        

    def get_user(self,obj):
        user = User.objects.get(id=obj.user.id)
        serializer = UserSerializer(user,many=False)
        return serializer.data

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ['id','user']
    
    
    
    def save(self,user=None):
        if user:
            validated_data = self.validated_data
            validated_data['user']=user
            print(validated_data.get('likes'))

            if validated_data.get('likes') is not None:
                validated_data.pop('likes')
            if validated_data.get('follower') is not None:
                validated_data.pop('follower')
            if validated_data.get('views') is not None:
                validated_data.pop('views')
            post = Post.objects.create(**validated_data)
            return post
        else:
            return super(PostSerializer,self).save()

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
    profile = ProfileSerializer()
    # tutorials = TutorialSerializer(read_only=True,many=True)
    # posts = PostSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields=['id','username','email','first_name','last_name','last_login','profile']
        read_only_fields = ['id','password','username']
  



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,validated_data):
        print(validated_data)
        username = validated_data.get('username','')
        password = validated_data.get('password','')
        print(username,password)
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