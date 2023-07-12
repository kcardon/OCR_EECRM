from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .permisions import EmployeePermission, ClientPermission, GroupPermission

from .models import Employee, Group, Client
from events.models import Event
from contracts.models import Contract
from .serializers import (
    EmployeeSerializer,
    EmployeeLoginSerializer,
    EmployeeSignUpSerializer,
    GroupSerializer,
    ClientSerializer,
)

from .filters import ClientFilter
import logging

logger = logging.getLogger(__name__)
# Create your views here.


class GroupAPIView(ModelViewSet):
    permission_classes = (GroupPermission,)
    serializer_class = GroupSerializer

    def get_object(self):
        try:
            obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
            self.check_object_permissions(self.request, obj)
            return obj
        except Http404:
            logger.error("Group with pk %s not found.", self.kwargs["pk"])
            return Response(
                {"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def get_queryset(self):
        return Group.objects.all()


class EmployeeAPIView(ModelViewSet):
    """return a list of app users"""

    permission_classes = (EmployeePermission,)
    serializer_class = EmployeeSerializer

    def get_object(self):
        try:
            obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
            self.check_object_permissions(self.request, obj)
            return obj
        except Http404:
            logger.error("Employee with pk %s not found.", self.kwargs["pk"])
            return Response(
                {"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def get_queryset(self):
        logger.debug("Attempting to connect to API")
        return Employee.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            "message": "Employee has been deleted",
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class EmployeeSignupAPIView(ModelViewSet):
    """allow registration API to create new user"""

    permission_classes = (EmployeePermission,)
    serializer_class = EmployeeSignUpSerializer

    def get_queryset(self):
        return Employee.objects.all()

    def post(self, request):
        serializer = EmployeeSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeLoginAPIView(TokenObtainPairView):
    """allow login and jwt tokens"""

    permission_classes = (AllowAny,)
    serializer_class = EmployeeLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            employee = serializer.validated_data["employee"]
            jwt_serializer = TokenObtainPairSerializer()
            token = jwt_serializer.get_token(employee)
            return Response(
                {
                    "username": employee.username,
                    "access": str(token.access_token),
                    "refresh": str(token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientAPIView(ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = (ClientPermission,)

    def get_object(self):
        try:
            obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
            self.check_object_permissions(self.request, obj)
            return obj
        except Http404:
            logger.error("Client with pk %s not found.", self.kwargs["pk"])
            return Response(
                {"error": "Client not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def get_queryset(self):
        group = self.get_user_group(self.request)
        if group == "Management":
            queryset = Client.objects.all()
        elif group == "Sales":
            queryset = Client.objects.filter(sales_contact=self.request.user)
        elif group == "Support":
            my_events = Event.objects.filter(support_contact=self.request.user)
            my_contracts = [event.contract for event in my_events]
            my_clients_ids = [contract.client.id for contract in my_contracts]
            queryset = Client.objects.filter(pk__in=my_clients_ids)
        filtered_queryset = ClientFilter(self.request.GET, queryset=queryset)
        return filtered_queryset.qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            "message": "Client has been deleted",
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    def get_user_group(self, request):
        return request.user.groups.all().values_list("name", flat=True).first()
