from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Queue(models.Model):
    name = models.CharField(max_length=256)
    current_number = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name + " Queue"

    def get_next_in_line(self):
        self.current_number += 1
        return self.current_number

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete='models.CASCADE')
    value = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username

    def payment(self):
        self.value -= 2
        self.save()