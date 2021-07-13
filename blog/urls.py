from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('posts',PostApiView,basename="post")
router.register('categories',CategoryApiView,basename="category")
router.register('users',UserApiView,basename="user")
router.register('comments',CommentApiView,basename="comment")
router.register('replies',ReplyApiView,basename="reply")
router.register('tutorials',TutorialApiView,basename="tutorial")
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('',include(router.urls)),
    path("user_login/",UserLoginApiView.as_view()),
    path("user_logout/",UserLogoutApiView.as_view()),
    path("user_register/",UserRegisterApiView.as_view()),
    path("upload-avatar/",UploadAvatarApiView.as_view()),
    path('user_refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
  

]
