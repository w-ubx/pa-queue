from django.urls import path

from queuer import views

app_name = 'queuer'

urlpatterns = [
    path('manager/', views.index, name='manager'),
]