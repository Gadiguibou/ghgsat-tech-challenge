from django.http import Http404, HttpResponse
from PIL import Image
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
import io

from .models import Target, Observation
from .renderers import JPEGRenderer, PNGRenderer
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


class TargetImage(APIView):
    """
    A view that returns a satelite image of the target.
    """

    renderer_classes = [JPEGRenderer, PNGRenderer]

    # TODO: Find a way to prevent repetition here.
    def get_object(self, pk):
        try:
            return Target.objects.get(pk=pk)
        except Target.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        target = self.get_object(pk)
        output = io.BytesIO()

        target.get_image().save(output, "PNG")

        return Response(output.getvalue())


class TargetResult(APIView):
    """
    A view that returns target's satelite image with the observation as an overlay.
    """

    renderer_classes = [JPEGRenderer, PNGRenderer]

    def get_object(self, pk):
        try:
            return Target.objects.get(pk=pk)
        except Target.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        target = self.get_object(pk)
        output = io.BytesIO()

        # This would normally use an associated observation file.
        # For now we'll just use the provided plume image.
        with Image.open("../plume.png") as overlay_img:
            target.overlay(target.get_image(), overlay_img).save(output, "PNG")

        return Response(output.getvalue())


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
