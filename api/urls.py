"""
URL configuration for cattleya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework import routers
from rest_framework.authtoken import views

from .activity.comment.models import ActivityCommentViewSet
from .activity.post.models import ActivityPostViewSet
from .blog.models import BlogViewSet, BlogTagViewSet
from .file.models import FileViewSet
from .models import UserViewSet, UserLoginAPIView, UserAvatarUploadView, UserLogoutAPIView
from .views import *

router = routers.DefaultRouter()
router.register(r'activity/posts', ActivityPostViewSet, basename="ActivityPost")
router.register(r'activity/comments', ActivityCommentViewSet, basename="ActivityComment")
router.register(r'users', UserViewSet, basename="User")
router.register(r'files', FileViewSet, basename="File")
router.register(r'blogs', BlogViewSet, basename="Blog")
router.register(r'blog-tags', BlogTagViewSet, basename="BlogTag")
urlpatterns = [
    # path('user/register', user_register),
    # path('user/login', user_login),
    # path('user/logout', user_logout),
    # path('user/info', user_info),
    # path('user/changepassword', user_change_password),
    # path('activity/post', activity_post),
    # path('activity/posts', activity_posts),
    # path('activity/comment', activity_comment),
    # path('activity/like', activity_like),
    path('auth/token', views.obtain_auth_token),
    path('auth/logout', csrf_exempt(UserLogoutAPIView.as_view())),
    path('auth/login', ensure_csrf_cookie(UserLoginAPIView.as_view())),
    path('user-avatar', csrf_exempt(UserAvatarUploadView.as_view())),
    path('', include(router.urls))
]
