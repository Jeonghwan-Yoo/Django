import os
import sys

# 프로젝트의 루트(베이스) 디렉토리를 지정합니다.
path = '/home/Jeonghwan/pyBook/ch7'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
