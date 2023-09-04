
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "NimishMac",
        "USER": "postgres",
        "PASSWORD": "Nimish@123",
        "HOST": "localhost".strip(),
        'PORT': '5436',
    }
}

#email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your_email'
EMAIL_HOST_PASSWORD = 'your_password'
EMAIL_PORT = 587 # also 25 , 465 or  587 can be used ,or any other  internal server setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#set to false in production
TEST_EMAIL_ENV = True
