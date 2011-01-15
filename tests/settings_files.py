import os.path

from settings import *
INSTALLED_APPS.append('files')

ROOT_URLCONF = 'files.urls'

MEDIA_ROOT = os.path.join(BASE_PATH, "files", "media")
MEDIA_URL = "/media/"
