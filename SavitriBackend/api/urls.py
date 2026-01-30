from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_pdf, name='upload_pdf'),
    path('topics', views.get_topics, name='get_topics'),
    path('generate', views.generate_audio, name='generate_audio'),
]
