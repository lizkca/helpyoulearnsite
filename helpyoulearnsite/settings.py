# ... 其他设置保持不变 ...

from django.utils.translation import gettext_lazy as _

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # 添加这行
    'django.middleware.common.CommonMiddleware',
    # ... 其他中间件 ...
]

LANGUAGES = [
    ('en', _('English')),
    ('zh-hans', _('Chinese')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]