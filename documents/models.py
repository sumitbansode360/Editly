from django.db import models
from shortuuidfield import ShortUUIDField
from django_ckeditor_5.fields import CKEditor5Field
from userauth.models import User

class Document(models.Model):
    uuid = ShortUUIDField(primary_key=True, auto=True)
    title = models.CharField(max_length=255)
    text=CKEditor5Field('Text', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return self.title


class Notification(models.Model):
    message = models.CharField(max_length=500)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
