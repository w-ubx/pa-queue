from django.contrib import admin

# Register your models here.
from .models import Queue, Wallet

admin.site.register(Queue)
admin.site.register(Wallet)
