from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .permisions import EmployeePermission, ClientPermission, GroupPermission

from .models import Employee, Group, Client

from .serializers import (
    EmployeeSerializer,
    EmployeeLoginSerializer,
    EmployeeSignUpSerializer,
    GroupSerializer,
    ClientSerializer,
)

# Create your views here.


class GroupAPIView(ModelViewSet):
    permission_classes = (GroupPermission,)
    serializer_class = GroupSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return Group.objects.all()


class EmployeeAPIView(ModelViewSet):
    """return a list of app users"""

    permission_classes = (EmployeePermission,)
    serializer_class = EmployeeSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return Employee.objects.all()


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
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return Client.objects.all()
