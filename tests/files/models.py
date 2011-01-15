import datetime
from django.contrib.auth.models import User
from django.db import models


class FileNote(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="uploads")
    
    def __unicode__(self):
        return u"FileNote %s" % self.name
