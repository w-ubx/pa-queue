from django.contrib import admin

# Register your models here.
from .models import Queue, Wallet, UserQueue

admin.site.register(Queue)
admin.site.register(Wallet)
admin.site.register(UserQueue)
