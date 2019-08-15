from django.db import models

# Create your models here.
class Queue(models.Model):
    name = models.CharField(max_length=256)
    current_number = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name + " Queue"

    def get_next_in_line(self):
        self.current_number += 1
        return self.current_number

