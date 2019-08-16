from django.urls import path

from face_recog import views

app_name = 'face_recog'
urlpatterns = [
    path('register/', views.register_face, name='register_face')
]