from django.db import models
from shortuuidfield import ShortUUIDField


class Document(models.Model):
    uuid = ShortUUIDField(primary_key=True, auto=True)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title
    