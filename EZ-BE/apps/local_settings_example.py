
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "dbuser",
        "USER": "dbusername",
        "PASSWORD": "dbpassword",
        "HOST": "localhost".strip(),
        'PORT': '5432',
    }
}

#email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'emailhost'
EMAIL_HOST_USER = 'emailuser@domain'
EMAIL_HOST_PASSWORD = 'emailpassword'
EMAIL_PORT = 587 # also 25 , 465 or  587 can be used ,or any other  internal server setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#set to false in production
TEST_EMAIL_ENV = True
