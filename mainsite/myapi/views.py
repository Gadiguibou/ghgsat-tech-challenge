from django.http import HttpResponse
from rest_framework import generics

from .models import Target, Observation
from .serializers import TargetSerializer, ObservationSerializer

# Basic index response for a friendlier message when reaching the index
def index(request):
    return HttpResponse("Hello from the index!")


class TargetList(generics.ListCreateAPIView):
    """
    List all currently registered targets or create a new one.
    """

    queryset = Target.objects.all()
    serializer_class = TargetSerializer


class TargetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update or delete a specific target using its primary key.
    """

    queryset = Target.objects.all()
    serializer_class = TargetSerializer
