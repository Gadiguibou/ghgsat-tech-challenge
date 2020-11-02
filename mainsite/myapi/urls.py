from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("targets/", views.TargetList.as_view()),
    path("targets/<int:pk>/", views.TargetDetail.as_view()),
]
