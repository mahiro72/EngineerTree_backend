from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'user'

router = DefaultRouter()
router.register('profile',views.ProfileViewSet)
router.register('study', views.StudyViewSet)
router.register('get_tweet', views.GetTweetViewSet)


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'), #最後に/つけないとエラーなる
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path("create_graph/", views.GraphCreateAPIView.as_view(), name="create_graph"),
    path("most_lang/", views.MostLangAPIView.as_view(), name="most_lang"),
    
    path('',include(router.urls)),
]

