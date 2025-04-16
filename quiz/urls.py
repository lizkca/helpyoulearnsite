from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('save-description/<int:image_id>/', views.save_description, name='save_description'),
]