"""
WSGI config for ResponsiveWebsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ResponsiveWebsite.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root='/ResponsiveWebsite/static/css/owl.carousel.min.css')
application = WhiteNoise(application, root='/ResponsiveWebsite/static/css/owl.theme.default.min.css')
application = WhiteNoise(application, root='/ResponsiveWebsite/static/css/fonts.css')
application = WhiteNoise(application, root='/ResponsiveWebsite/static/css/style.css')
application = WhiteNoise(application, root='/ResponsiveWebsite/static/css/aos.css')
application = WhiteNoise(application, root='/ResponsiveWebsite/static/css/all.css')
application = WhiteNoise(application, root='/ResponsiveWebsite/static/css/default.css')
application.add_files('/ResponsiveWebsite/staticfiles', prefix='staticfiles/')
