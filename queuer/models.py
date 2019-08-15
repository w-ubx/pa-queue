from django.db import models
from django.contrib.auth.models import User


class Queue(models.Model):
    name = models.CharField(max_length=256)
    current_number = models.PositiveIntegerField()
    latest_assigned = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name + " Queue"

    def get_next_in_line(self):
        self.current_number += 1
        return self.current_number


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete='models.CASCADE', related_name='wallet')
    value = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username

    def payment(self):
        self.value -= 3
        self.save()


class UserQueue(models.Model):
    user = models.ForeignKey(User, on_delete='models.CASCADE')
    queue = models.ForeignKey(Queue, on_delete='models.CASCADE')
    number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s - %s" % (self.user.username, self.queue)

    def assign_number(self):
        self.number = self.queue.latest_assigned + 1
        self.save()

        self.queue.latest_assigned += 1
        self.queue.save()
