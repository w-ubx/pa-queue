from django.urls import path

from queuer import views

app_name = 'queuer'
urlpatterns = [
    path('queues/<int:queue_id>/', views.detail, name='detail'),
    path('current_number/<int:queue_id>/', views.current_number, name='current_number'),
    path('api/increment/', views.increment, name='increment'),
    path('get_wallet/', views.get_wallet, name='get_wallet'),
    path('assign_number/', views.assign_number, name='assign_number'),
    path('', views.listing, name='listing'),
    path('login/', views.login, name='login')
]
