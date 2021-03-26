from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path("^service_tree/genres/$", views.show_genres),
    path("v1/service_tree/unlink/<int:pk>/", views.UnlinkNodeServerApiView.as_view()),
    path("v1/service_tree/parents/<int:pk>/", views.ParentNodeInfoApiView.as_view()),
]
