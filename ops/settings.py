"""
Django settings for ops project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import ldap
import datetime
from config.config import LightningOpsConfig as Config
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(ROOT_DIR, 'apps')
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@yuwoez1o&oqwyt-1t%v$n5dc0iww0uo3)7^tg&0&z5e9_po5o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = Config.DEBUG

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 内部
    "apps.cmdb.apps.CmdbConfig",
    "apps.user.apps.UserConfig",
    "apps.service_tree.apps.ServiceTreeConfig",
    "apps.audit.apps.AuditConfig",
    "apps.tasks.apps.TasksConfig",
    "apps.permission.apps.PermissionConfig",


    # 第三方
    "rest_framework",
    "drf_yasg",
    "django_filters",
    "mptt",
    "corsheaders",
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 自定义
    "middleware.audit.EventAuditMiddleware",
]

ROOT_URLCONF = 'ops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(ROOT_DIR, "templates")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": Config.MYSQL_DB,
        "USER": Config.MYSQL_USER,
        "PASSWORD": Config.MYSQL_PASSWORD,
        "HOST": Config.MYSQL_HOST,
        "PORT": Config.MYSQL_PORT,
        "OPTIONS": {
            "charset": Config.MYSQL_CHARSET,
            "unix_socket": Config.MYSQL_UNIX_SOCKET,
            'init_command': "SET sql_mode='traditional'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = "zh-hans"

# TIME_ZONE = 'UTC'
TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = False

# 以标准的datetime.now()时间保持一致.
# 上海的UTC时间
USE_TZ = False

DATETIME_FORMAT = 'Y年n月j日 H:i:s'
DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# 参考 https://blog.csdn.net/u013451157/article/details/78376187
STATIC_URL = '/static/'

# python manage.py collectstatic
STATIC_ROOT = os.path.join(ROOT_DIR, "static/")

# 追加新的配置文件

# DRF
REST_FRAMEWORK = {
    # 自定义异常
    'EXCEPTION_HANDLER': 'base.exceptions.custom_exception_handler',
    # 配置后端搜索
    # "DEFAULT_FILTER_BACKENDS": {
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # },
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
}

# User扩展
AUTH_USER_MODEL = "user.UserProfile"

# JWT
# https://jpadilla.github.io/django-rest-framework-jwt/
JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300000),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),
}

# CORS
# CORS 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.0:8000',
    'http://121.4.224.236:8000',
)

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'XMLHttpRequest',
    'X_FILENAME',
    'Pragma',
]

# 日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(process)d] [%(thread)d] [%(filename)16s:%(lineno)4d] [%(levelname)-6s] %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'main': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(module)s %(levelname)s] %(message)s',
        },
        'exception': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '\n%(asctime)s [%(levelname)s] %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'syslog': {
            'format': 'jumpserver: %(message)s'
        },
        'msg': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main'
        },
        'file': {
            'encoding': 'utf8',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*100,
            'backupCount': 7,
            'formatter': 'default',
            'filename': Config.OPS_LOG_FILE,
        },
        'ansible_logs': {
            'encoding': 'utf8',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'main',
            'maxBytes': 1024*1024*100,
            'backupCount': 7,
            'filename': Config.ANSIBLE_LOG_FILE,
        },
        'drf_exception': {
            'encoding': 'utf8',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'exception',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 7,
            'filename': Config.DRF_EXCEPTION_LOG_FILE,
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.NullHandler',
            'formatter': 'syslog'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': Config.LOG_LEVEL,
        },
        'django.request': {
            'handlers': ['console', 'file', 'syslog'],
            'level': Config.LOG_LEVEL,
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file', 'syslog'],
            'level': Config.LOG_LEVEL,
            'propagate': False,
        },
        'drf_exception': {
            'handlers': ['console', 'drf_exception'],
            'level': Config.LOG_LEVEL,
        },
        'ops.ansible_api': {
            'handlers': ['console', 'ansible_logs'],
            'level': Config.LOG_LEVEL,
        },
        'django_auth_ldap': {
            'handlers': ['console', 'file'],
            'level': "INFO",
        },
        'syslog': {
            'handlers': ['syslog'],
            'level': 'INFO'
        },
    }
}

# admin role
ADMIN_ROLE = "admin:role"

# celery
CELERY_BROKER_URL = 'redis://:{}@{}:{}/6'.format(Config.REDIS_PASSWORD, Config.REDIS_HOST, Config.REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://:{}@{}:{}/7'.format(Config.REDIS_PASSWORD, Config.REDIS_HOST, Config.REDIS_PORT)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False

# Ansible
ANSIBLE_HOSTS_PATH = "/etc/ansible/hosts/hosts"
ANSIBLE_SCRIPT_PATH = "/data/tasks"


# LDAP
# https://github.com/django-auth-ldap/django-auth-ldap
# LDAP 服务地址
AUTH_LDAP_SERVER_URI = "ldap://{}:{}".format(Config.LDAP_SERVER_URI, Config.LDAP_SERVER_PORT)

# 需要使用这个去验证其他用户名的准确性 cn=admin,ou=staff,dc=nucarf,dc=cn
AUTH_LDAP_BIND_DN = Config.AUTH_LDAP_BIND_DN
AUTH_LDAP_BIND_PASSWORD = Config.AUTH_LDAP_BIND_PASSWORD

# 允许认证用户的路径 cn=admin,ou=staff,dc=nucarf,dc=cn
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    Config.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(cn=%(user)s)"  # 邮箱登录 指定ou下的用户
)

# 当ldap用户登录时，从ldap的用户属性对应写到django的user数据库，键为django的属性，值为ldap用户的属性
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "cn",
    "name": "displayName",
    "email": "email",
}

# 如果为True，则每次用户登录时，将使用LDAP目录中的最新值来更新用户对象的字段。
# 否则，仅在自动创建用户对象时填充该用户对象。
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Cache distinguished names and group memberships for an hour to minimize
# LDAP traffic.
AUTH_LDAP_CACHE_TIMEOUT = 3600

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    "django_auth_ldap.backend.LDAPBackend",  # 优先使用ldap进行用户验证
    "django.contrib.auth.backends.ModelBackend",
)

# drf-extensions
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_BULK_OPERATION_HEADER_NAME': 'X-CUSTOM-BULK-OPERATION'
}


INTERNAL_IPS = [
    '127.0.0.1',
]