from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework_simplejwt.views import TokenVerifyView
from . import views

urlpatterns = [
    path('index/',views.index, name='users_main_view'),
    path('signup/', views.signup, name='users_signup'),
    path('create_user/', views.create_user, name="create_user_api"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh_api"),
    path('token/verify/', TokenVerifyView.as_view(), name="token_verify_api"),
    path('login/', TokenObtainPairView.as_view(), name="login_api"),
    path('list/', views.user_list, name="user_list_api"),

    # Path Param
    # https://localhost:8000/users/1/

    # Query Param
    # https://localhost:8000/users/get/?id=1
    path('<int:pk>/', views.UserProfileDetail.as_view(), name='user_profile_detail'),
    path('edge/', views.UserNetworkEdgeView.as_view(), name='user_network_edge'),
]