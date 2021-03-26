"""ops URL Configuration

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
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

# JWT
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
]

# JWT
urlpatterns += [
    path('api/v1/api-token-auth/', obtain_jwt_token),
    path('api/v1/api-token-refresh/', refresh_jwt_token),
    path('api/v1/api-token-verify/', verify_jwt_token),

]

# router
from apps.user.router import router as user_router
from apps.audit.router import router as audit_router
from apps.tasks.router import router as tasks_router
from apps.service_tree.router import router as service_tree_router
from apps.permission.router import router as permission_router
from apps.cmdb.router import router as cmdb_router
# from apps.cron.router import router as cron_router

router = routers.DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(audit_router.registry)
router.registry.extend(service_tree_router.registry)
router.registry.extend(permission_router.registry)
router.registry.extend(cmdb_router.registry)
router.registry.extend(tasks_router.registry)
# router.registry.extend(cron_router.registry)

urlpatterns += [
    path('api/', include(router.urls)),
]

# apps urls
from apps.user import urls as user_url
from apps.service_tree import urls as service_tree_url
from apps.permission import urls as permission_url
from apps.tasks import urls as tasks_urls
urlpatterns += [
    path('api/', include(router.urls)),
    path('api/', include(user_url)),
    path('api/', include(tasks_urls)),
    path('api/', include(service_tree_url)),
    path('api/', include(permission_url)),
]

# DOCS
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Ops API",
        default_version='v1',
        description="Document description",
        terms_of_service="http://www.aiops724.com/",
        contact=openapi.Contact(email="monkey@ops.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]





