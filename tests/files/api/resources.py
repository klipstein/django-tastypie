from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from files.models import FileNote

class FileNoteResource(ModelResource):
    
    class Meta:
        resource_name = 'filenotes'
        queryset = FileNote.objects.all()
        authorization = Authorization()
