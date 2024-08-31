from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch_characters', views.fetch_characters, name='fetch_characters'),
    path('dataset/<int:id>', views.show_dataset, name='show_dataset')
]
