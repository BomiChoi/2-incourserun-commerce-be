from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = "user"

urlpatterns = [
    path("/me", views.MeDetailUpdateDeleteView.as_view()),
    path("/me/carts", views.MeCartListView.as_view()),
    path("/me/orders", views.MeOrderListView.as_view()),
    path("/me/reviews", views.MeReviewListView.as_view()),
    path('/social_login', views.UserSocialLoginView.as_view()),
    path('/withdrawal',views.UserWithdrawalListCreateView.as_view()),
    path('/withdrawal/<int:pk>',views.UserWithdrawalUpdateDeleteView.as_view()),
    path('/token/refresh', TokenRefreshView.as_view()),
    path('/login/kakao', views.kakao_login)
]