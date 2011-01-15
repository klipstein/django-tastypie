from django.conf.urls.defaults import *
from tastypie.api import Api
from files.api.resources import FileNoteResource

api = Api(api_name='v1')
api.register(FileNoteResource(), canonical=True)

urlpatterns = api.urls
