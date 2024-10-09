from django.urls import path
from . import views
urlpatterns = [
    path('', views.api_lists, name='api_lists'),
    path('get_time/', views.get_time, name='get_time'),
    path('todos/', views.to_dos, name='todo'),
    path('get_todo/<str:pk>', views.get_todo, name='get_todo'),
    path('create_todo/', views.create_todo, name='create_todo'),
    path('update_todo/<str:pk>', views.update_todo, name='update_todo'),
    path('delete_todo/<str:pk>', views.delete_todo, name='delete_todo')
    
]
