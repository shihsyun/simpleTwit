"""simpleTwit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from simpleTwit import views


urlpatterns = [
    path('api/register/', views.Register,
         name='register'),
    path('api/login/', views.Login,
         name='login'),
    path('api/logout/', views.Logout,
         name='logout'),
    path('api/createtwit/', views.CreateTwit,
         name='createtwit'),
    path('api/createcomment/', views.CreateComment,
         name='createcomment'),
    path('api/likeit/', views.CreateLikeit,
         name='likeit'),
    path('api/destorylikeit/', views.DestoryLikeit,
         name='destorylikeit'),
    path('api/twits/<int:pk>/', views.TwitDetail,
         name='twitdetail'),
    path('api/comments/<int:pk>/', views.CommentDetail,
         name='commentdetail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
