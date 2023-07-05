from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_date

from rest_framework.viewsets import ModelViewSet
from .serializers import EventSerializer, EventStatusSerializer
from .models import Event, EventStatus
from .permissions import EventPermission, EventStatusPermission
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class EventAPIView(ModelViewSet):
    """return a list of app users"""

    permission_classes = (EventPermission,)
    serializer_class = EventSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        contract_id = self.kwargs.get("contract_id")
        if contract_id is not None:
            queryset = Event.objects.filter(contract=contract_id)
        else:
            queryset = Event.objects.all()

        client_name = self.request.GET.get("client_name")
        if client_name is not None:
            queryset = queryset.filter(client__last_name__icontains=client_name)

        client_email = self.request.GET.get("client_email")
        if client_email is not None:
            queryset = queryset.filter(client__email__icontains=client_email)

        date_before = self.request.GET.get("date_before")
        if date_before is not None:
            date_before = parse_date(date_before)
            queryset = queryset.filter(event_date__lte=date_before)  # less or equal

        date_after = self.request.GET.get("date_after")
        if date_after is not None:
            date_after = parse_date(date_after)
            queryset = queryset.filter(event_date__gte=date_after)  # greater or equal

        return queryset

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
