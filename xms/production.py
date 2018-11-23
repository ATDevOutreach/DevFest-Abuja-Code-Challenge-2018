import * from .settings

DEBUG = False
AT_USERNAME = os.environ.get('AT_USERNAME')
AT_API_KEY = os.environ.get('AT_API_KEY')
AT_PRODUCT_NAME = os.environ.get('AT_PRODUCT_NAME')
ALLOWED_HOSTS = ['https://x-m-s.herokuapp.com/',]
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
django_heroku.settings(locals())
