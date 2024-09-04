from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("fetch_characters", views.fetch_characters, name="fetch_characters"),
    path("dataset/<int:id>", views.show_dataset, name="show_dataset"),
    path("dataset/<int:id>/aggregate", views.show_dataset_aggregate, name="show_dataset_aggregate"),
]
