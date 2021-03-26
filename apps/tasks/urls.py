from django.urls import path, re_path

from . import views


urlpatterns = [
    # 执行ansible script/ playbook
    path('v1/tasks/exec/command', views.ExecCommandApiView.as_view()),

    # 获取脚本和playbook
    path('v1/tasks/scripts_playbook', views.ScriptPlaybookApiView.as_view()),
    path('v1/tasks/scripts_playbook/<str:filename>/', views.ScriptPlaybookApiView.as_view()),
]
