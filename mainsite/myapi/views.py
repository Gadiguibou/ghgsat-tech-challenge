from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

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


class ObservationList(APIView):
    """
    List all currently registered observations or create a new one.
    """

    # Needed to retrieve the image from the request
    parser_classes = [MultiPartParser, FormParser]

    # Return a list of all observations
    def get(self, request, format=None):
        observations = Observation.objects.all()
        serializer = ObservationSerializer(targets, many=True)
        return Response(serializer.data)

    # Add a new observation
    def post(self, request, format=None):
        serializer = ObservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObservationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update or delete a specific observation using its primary key.
    """

    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
