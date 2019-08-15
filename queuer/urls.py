from django.urls import path

from queuer import views

app_name = 'queuer'
urlpatterns = [
    path('queues/<int:queue_id>/', views.detail, name='detail'),
    path('api/increment/', views.increment, name='increment'),
    path('', views.listing, name='listing'),
]
