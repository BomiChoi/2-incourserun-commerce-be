from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('', views.UserListView.as_view()),
    path('/<int:pk>', views.UserDetailUpdateDeleteView.as_view()),
    path('/social_login', views.UserSocialLoginView.as_view()),
    path('/social', views.SocialListCreateView.as_view()),
    path('/social/<int:pk>', views.SocialDetailUpdateDeleteView.as_view()), 
    path('/cart', views.CartListCreateView.as_view()),
    path('/cart/<int:pk>', views.CartDetailUpdateDeleteView.as_view()),
    path('/login/kakao', views.kakao_login),
    path('/login/kakao/callback', views.kakao_callback)
]