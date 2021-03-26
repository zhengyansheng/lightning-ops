from django.urls import path
from . import views


urlpatterns = [
    path('v1/corp/user/info', views.UserInfoApiView.as_view(), name='user_info'),
]