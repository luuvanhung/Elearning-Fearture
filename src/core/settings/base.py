import os
from os.path import join

from corsheaders.defaults import default_headers

from api_oauth2.utils import signed_token_generator
from common.constants.api_constants import HttpMethod
from utils import read_scopes
from . import env, BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = (
    os.environ["SECRET_KEY"] if "SECRET_KEY" in os.environ else env("SECRET_KEY")
)
API_HOST = env("API_HOST")
API_PORT = env("API_PORT")
OAUTH2_SCHEME = "http" if API_HOST in ["localhost", "127.0.0.1"] else "https"
OAUTH2_PORT = ":" + API_PORT if API_PORT is not None else ""
OAUTH2_URL = OAUTH2_SCHEME + "://" + API_HOST + OAUTH2_PORT
CUSTOM_DOMAIN = env("CUSTOM_DOMAIN")
UI_HOST = env("UI_HOST")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[API_HOST, "api", "localhost"])
USE_X_FORWARDED_HOST = env.bool("USE_X_FORWARDED_HOST", default=False)
ALLOWED_SWAGGER = env.bool("ALLOWED_SWAGGER", default=True)
# Application definition
DJANGO_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)
THIRD_PARTY_APPS = (
    "rest_framework",
    "rest_framework_api_key",
    "corsheaders",
    "django_crontab",
    "django_filters",
    "bandit",
    "django_nose",
    "webpack_loader",
    "oauth2_provider",
    "drf_yasg",
    "binary_database_files",
)
LOCAL_APPS = (
    "api",
    "api_base",
    "api_user",
    "api_admin",
    "api_team",
    "api_workday",
    "api_probation",
    "api_providers",
    "api_lunch",
    "api_user_lunch",
    "api_event",
    "api_oauth2",
    "api_skill",
    "api_office",
    "api_session",
    "api_seat_map",
    "health_check",
    "api_wfh",
    "api_slackbot",
    "api_authservices",
    "api_elearning"
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = "api_user.User"

# Config django-cors lib

CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://127.0.0.1:8001",
        "http://localhost:8001",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
)

CORS_ALLOW_METHODS = [
    HttpMethod.DELETE,
    HttpMethod.GET,
    HttpMethod.OPTIONS,
    HttpMethod.PATCH,
    HttpMethod.POST,
    HttpMethod.PUT,
]
# CORS_URLS_REGEX = r"^/api/.*$"
CORS_ALLOW_HEADERS = list(default_headers)

# Static files
STATIC_ROOT = join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "dist", "static"),
]

# Media files
MEDIA_ROOT = join(BASE_DIR, "media")
MEDIA_URL = "/media/"
MEDIA_IMAGE = f"{CUSTOM_DOMAIN}"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
X_FRAME_OPTIONS = 'SAMEORIGIN'
# config oauth2
PRIVATE_KEY_FILE = env("PRIVATE_KEY_FILE", default="jwt")
PRIVATE_KEY_PATH = join(BASE_DIR, PRIVATE_KEY_FILE)
SCOPES_JSON_PATH = join(BASE_DIR, "scopes.json")
DEFAULT_SCOPES_JSON_PATH = join(BASE_DIR, "default-scopes.json")
with open(PRIVATE_KEY_PATH) as f:
    PRIVATE_PEM = f.read()
with open(PRIVATE_KEY_PATH + ".pub") as f:
    PUBLIC_KEY = f.read()
SCOPES: dict = read_scopes(SCOPES_JSON_PATH)
DEFAULT_SCOPES: dict = read_scopes(DEFAULT_SCOPES_JSON_PATH)

OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_EXPIRE_SECONDS": 3600,
    # "SCOPES_BACKEND_CLASS": "api_oauth2.scopes.ScopesBackend",
    "ACCESS_TOKEN_GENERATOR": signed_token_generator(PRIVATE_PEM, issuer="damelagi"),
    "REFRESH_TOKEN_GENERATOR": "oauthlib.oauth2.rfc6749.tokens.random_token_generator",
    "OAUTH2_VALIDATOR_CLASS": "api_oauth2.pre_configured.CustomOAuth2Validator",
    "ROTATE_REFRESH_TOKEN": True,
    "REFRESH_TOKEN_GRACE_PERIOD_SECONDS": 4000,
    "SCOPES": SCOPES,
    "DEFAULT_SCOPES": DEFAULT_SCOPES,
}
# Application config
APP_NAME = env.str("APP_NAME", default="HRM")
SUPER_ADMIN_EMAIL = env.str("SUPER_ADMIN_EMAIL", default="superadmin@gmail.com")
SUPER_ADMIN_PASSWORD = env.str("SUPER_ADMIN_PASSWORD")
NBF_TIME = 0
DEFAULT_CLIENT_SECRET = (
    os.environ["DEFAULT_CLIENT_SECRET"]
    if "DEFAULT_CLIENT_SECRET" in os.environ
    else env("DEFAULT_CLIENT_SECRET")
)
DEFAULT_CLIENT_ID = (
    os.environ["DEFAULT_CLIENT_ID"]
    if "DEFAULT_CLIENT_ID" in os.environ
    else env("DEFAULT_CLIENT_ID")
)
OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = "api_oauth2.AccessToken"
OAUTH2_PROVIDER_APPLICATION_MODEL = "api_oauth2.Application"
OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = "api_oauth2.RefreshToken"
OAUTH2_PROVIDER_GRANT_MODEL = "api_oauth2.Grant"
OAUTH2_PROVIDER_ID_TOKEN_MODEL = "api_oauth2.IDToken"

AUTHENTICATION_BACKENDS = (
    "api_oauth2.backends.CustomOAuth2Backend",
    "django.contrib.auth.backends.ModelBackend",  # To keep the Browsable API
)

# Config Django Rest framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "api_oauth2.permissions.oauth2_permissions.TokenHasActionScope"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "api.pagination.CustomPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# Testing
# Use nose to run all tests
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

# Tell nose to measure coverage on the "foo" and "bar" apps
NOSE_ARGS = [
    "--with-coverage",
    "--cover-package=api_user_lunch,api_lunch",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
def db_config(prefix="", test=None):
    if test is None:
        test = {}
    DB_NAME = os.environ["DB_NAME"] if "DB_NAME" in os.environ else env("DB_NAME")
    return {
        "ENGINE": "django.db.backends.mysql",
        "NAME": prefix + DB_NAME,
        "USER": os.environ["DB_USER"] if "DB_USER" in os.environ else env("DB_USER"),
        "PASSWORD": os.environ["DB_PASSWORD"]
        if "DB_PASSWORD" in os.environ
        else env("DB_PASSWORD"),
        "HOST": os.environ["DB_HOST"] if "DB_HOST" in os.environ else env("DB_HOST"),
        "PORT": os.environ["DB_PORT"] if "DB_PORT" in os.environ else env("DB_PORT"),
        "TEST": test,
        "OPTIONS": {"charset": "utf8mb4"},
    }


# Backup Database
REPLICATION_DB_ALIAS = "replication"
REPLICATION_PREFIX = env("REPLICATION_DB_PREFIX", default="")

DATABASES = {
    "default": db_config(),
    "tests": db_config("", {"MIRROR": "default"}),
    REPLICATION_DB_ALIAS: db_config(REPLICATION_PREFIX),
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = env("LANGUAGE_CODE", default="en-us")
TIME_ZONE = "Asia/Ho_Chi_Minh"

USE_I18N = True

USE_L10N = True
USE_TZ = False

# EMAIL related settings
GRANTED_MAIL = [env("DEV_MAIL")]

BANDIT_WHITELIST = GRANTED_MAIL
BANDIT_EMAIL = ""

URL_WEB_INTERNAL = env("WEB_INTERNAL", default="https://hrm.dev.damelagi.org")

CALENDAR_ID = env("CALENDAR_ID")

LINK_EVENT_SYSTEM = env("LINK_EVENT_SYSTEM")

# SLACK
SLACK_CLIENT_ID = env("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = env("SLACK_CLIENT_SECRET")
SLACK_USER_OAUTH_TOKEN = env("SLACK_USER_OAUTH_TOKEN")
SLACK_BOT_USER_OAUTH_TOKEN = env("SLACK_BOT_USER_OAUTH_TOKEN")
SLACK_DEFAULT_CHANNEL = env("SLACK_DEFAULT_CHANNEL")
SLACK_LEAVE_CHANNEL = env("SLACK_LEAVE_CHANNEL")
SLACK_LUNCH_CHANNEL = env("SLACK_LUNCH_CHANNEL")

CRONJOBS = [
    ("0 0 15 12 *", "api_workday.cron_tab.create_remain_leave_for_next_year"),
    ("* * 1 * *", "api_workday.cron_tab.add_annual_leave"),
    ("* 08 * * *", "api_workday.cron_tab.get_leave_today"),
    ("* * 28 * *", "api_user_lunch.cron_tab.set_lunch_auto_next_month"),
    ("* 9,15 * * *", "api_probation.cron_tab.get_probation_reminder_today"),
    ("0 9 * * *", "api_user_lunch.cron_tab.send_notification_about_lunch"),
    ("0 9 * * *", "api_elearning.cron_tab.send_assignments_reminder"),
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL", default="Management Admin <noreply@damelagi.org>"
)
DEFAULT_EMAIL_ADMIN = env("DEFAULT_EMAIL_ADMIN", default="noreply@damelagi.org")
BLOCKED_EMAIL_DOMAINS = env.list(
    "BLOCKED_EMAIL_DOMAINS",
    default=[
        "paradox.ai",
    ],
)

SLACK_BOT_USER_ID = env("SLACK_BOT_USER_ID")
DEV_SLACK_USER_ID = env("DEV_SLACK_USER_ID")
DEV_LINE_MANAGER_SLACK_USER_ID = env("DEV_LINE_MANAGER_SLACK_USER_ID")
HRM_NEW_LEAVE_REQUEST_LINK = env("HRM_NEW_LEAVE_REQUEST_LINK")
HRM_NEW_WFH_REQUEST_LINK = env("HRM_NEW_WFH_REQUEST_LINK")
HRM_LEAVE_REQUEST_LINK = env("HRM_LEAVE_REQUEST_LINK")
HRM_APPROVAL_REQUEST_LINK = env("HRM_APPROVAL_REQUEST_LINK")

WIT_API_VERSION = "20211220"
WIT_TOKEN = env("WIT_TOKEN")
ENVIRONMENT = env("ENVIRONMENT")
INTENT_THRESHOLD = env("INTENT_THRESHOLD")
USE_INVITE_ATTENDEES_GOOGLE = env.bool("USE_INVITE_ATTENDEES_GOOGLE", default=False)

EMAIL_DOMAIN = env("EMAIL_DOMAIN")
LIMIT_DOMAIN = env.bool("LIMIT_DOMAIN")

# AWS config
AWS_ACCESS_KEY_ID = (
    os.environ["AWS_ACCESS_KEY_ID"]
    if "AWS_ACCESS_KEY_ID" in os.environ
    else env("AWS_ACCESS_KEY_ID")
)
AWS_SECRET_ACCESS_KEY = (
    os.environ["AWS_SECRET_ACCESS_KEY"]
    if "AWS_SECRET_ACCESS_KEY" in os.environ
    else env("AWS_SECRET_ACCESS_KEY")
)
AWS_STORAGE_BUCKET_NAME = (
    os.environ["AWS_STORAGE_BUCKET_NAME"]
    if "AWS_STORAGE_BUCKET_NAME" in os.environ
    else env("AWS_STORAGE_BUCKET_NAME")
)

AWS_S3_REGION_NAME = (
    os.environ["AWS_S3_REGION_NAME"]
    if "AWS_S3_REGION_NAME" in os.environ
    else env("AWS_S3_REGION_NAME")
)
AWS_S3_REGION_NAME = (
    None
    if AWS_S3_REGION_NAME is not None and len(AWS_S3_REGION_NAME.strip()) == 0
    else AWS_S3_REGION_NAME.strip()
)

STORE_USER_FILES_ON_S3 = (
    bool(os.environ["STORE_USER_FILES_ON_S3"])
    if "STORE_USER_FILES_ON_S3" in os.environ
    else env.bool("STORE_USER_FILES_ON_S3", default=False)
)
if STORE_USER_FILES_ON_S3:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_QUERYSTRING_AUTH = True
    AWS_DEFAULT_ACL = None
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
else:
    DEFAULT_FILE_STORAGE = "binary_database_files.storage.DatabaseStorage"
    DB_FILES_AUTO_EXPORT_DB_TO_FS = False
    DATABASE_FILES_URL_METHOD = "URL_METHOD_2"
