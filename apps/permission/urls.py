from . import views

from django.urls import path

urlpatterns = [
    path('v1/has-perm', views.HasPermissionView.as_view()),
    path('v1/route', views.UserGetRoute.as_view()),
]