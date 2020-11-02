from django.urls import path

from . import views

urlpatterns = [
    # API index
    path("", views.index, name="index"),
    # Targets
    path("targets/", views.TargetList.as_view()),
    path("targets/<int:pk>/", views.TargetDetail.as_view()),
    path("targets/<int:pk>/show/", views.TargetImage.as_view()),
    path("targets/<int:pk>/result/", views.TargetResult.as_view()),
    # Observations
    path("observations/", views.ObservationList.as_view()),
    path("observations/<int:pk>/", views.ObservationDetail.as_view()),
    path("observations/<int:pk>/show/", views.ObservationImage.as_view()),
    path("observations/<int:pk>/result/", views.ObservationResult.as_view()),
]
