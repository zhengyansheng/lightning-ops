import os


class Config(object):
    """Base config class."""

    DEBUG = True

    # MYSQL Default
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "12345678"
    MYSQL_DB = "lightning-ops2"
    MYSQL_CHARSET = "utf8mb4"
    MYSQL_UNIX_SOCKET = ""

    # REDIS Default
    REDIS_HOST = "127.0.0.1"
    REDIS_PASSWORD = ""
    REDIS_PORT = 6379

    # Logging
    OPS_LOG_FILE = "logs/ops.log"
    ANSIBLE_LOG_FILE = "logs/ansible.log"
    DRF_EXCEPTION_LOG_FILE = "logs/drf_exception.log"
    LOG_LEVEL = "DEBUG"

    # LDAP
    LDAP_SERVER_URI = "127.0.0.1"
    LDAP_SERVER_PORT = 389
    AUTH_LDAP_BIND_DN = ""
    LDAP_BASE_DN = ""
    AUTH_LDAP_BIND_PASSWORD = ""


class DevelopmentConfig(Config):
    """Development config class."""

    DEBUG = True

    # MYSQL Default
    MYSQL_HOST = "www.aiops724.com"
    MYSQL_PORT = 3306
    MYSQL_USER = "lightning_user"
    MYSQL_PASSWORD = "12345678"
    MYSQL_DB = "lightning"
    MYSQL_CHARSET = "utf8mb4"
    MYSQL_UNIX_SOCKET = ""


class ProductionConfig(Config):
    """Production config class."""

    DEBUG = False

    # MYSQL Default
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_DB = "lightning-ops2"
    MYSQL_CHARSET = "utf8mb4"
    MYSQL_UNIX_SOCKET = ""

    # REDIS Default
    REDIS_HOST = "127.0.0.1"
    REDIS_PASSWORD = ""
    REDIS_PORT = 6379


if os.environ.get("OPS_APP_ENV") == "release":
    LightningOpsConfig = ProductionConfig()
else:
    LightningOpsConfig = DevelopmentConfig()
