from django.db import models

class Contract(models.Model):
    user = models.CharField(max_length=42)
    queue_id = models.IntegerField(default=0)
    number = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % self.name
