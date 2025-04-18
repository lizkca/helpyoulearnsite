from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('learn-with-images/', views.learn_with_images, name='learn_with_images'),
    path('practice-pronunciation/', views.practice_pronunciation, name='practice_pronunciation'),
    path('save-description/<int:image_id>/', views.save_description, name='save_description'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('my-descriptions/', views.my_descriptions, name='my_descriptions'),
]