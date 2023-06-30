from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .permisions import EmployeePermission, ClientPermission

from .models import Employee, Group, Client

from .serializers import EmployeeSerializer, EmployeeLoginSerializer, EmployeeSignUpSerializer, GroupSerializer, ClientSerializer
# Create your views here.

class GroupAPIView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    def get_queryset(self):
        return Group.objects.all()
    
class EmployeeAPIView(ModelViewSet):
    """return a list of app users"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EmployeeSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_queryset(self):
        return Employee.objects.all()
    
class EmployeeSignupAPIView(ModelViewSet):
    """allow registration API to create new user"""

    serializer_class = EmployeeSignUpSerializer
    permission_classes = (AllowAny,)

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

    serializer_class = EmployeeLoginSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            jwt_serializer = TokenObtainPairSerializer()
            token = jwt_serializer.get_token(user)
            return Response(
                {
                    "username": user.username,
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