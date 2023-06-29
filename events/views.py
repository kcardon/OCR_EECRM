from django.shortcuts import render,get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .serializers import EventSerializer, EventStatusSerializer
from .models import Event, EventStatus
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class EventAPIView(ModelViewSet):
    """return a list of app users"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_queryset(self):
        return Event.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            "message": "Event has been deleted",
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
    
class EventStatusAPIView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class= EventStatusSerializer
    def get_queryset(self):
        return EventStatus.objects.all()