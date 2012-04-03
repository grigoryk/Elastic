import os, sys
sys.path.append('/Users/grisha/Code/django-trunk/django')
sys.path.append('/Users/grisha/Code')
sys.path.append('/Users/grisha/Code/elastic')
os.environ['DJANGO_SETTINGS_MODULE'] = 'elastic.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()