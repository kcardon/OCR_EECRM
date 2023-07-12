from django.shortcuts import render, get_object_or_404
from django.http import Http404

from django.utils.dateparse import parse_date

from rest_framework.viewsets import ModelViewSet
from .serializers import EventSerializer, EventStatusSerializer
from .models import Event, EventStatus
from .permissions import EventPermission, EventStatusPermission
from .filters import EventFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class EventAPIView(ModelViewSet):
    """return a list of app users"""

    permission_classes = (EventPermission,)
    serializer_class = EventSerializer

    def get_object(self):
        try:
            obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
            self.check_object_permissions(self.request, obj)
            return obj
        except Http404:
            logger.error("Event with pk %s not found.", self.kwargs["pk"])
            return Response(
                {"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def get_queryset(self):
        contract_id = self.kwargs.get("contract_id")
        if contract_id is not None:
            queryset = Event.objects.filter(contract=contract_id)
        else:
            queryset = Event.objects.all()

        filtered_queryset = EventFilter(self.request.GET, queryset=queryset)
        return filtered_queryset.qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            "message": "Event has been deleted",
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class EventStatusAPIView(ModelViewSet):
    permission_classes = (EventPermission,)
    serializer_class = EventStatusSerializer

    def get_queryset(self):
        return EventStatus.objects.all()
