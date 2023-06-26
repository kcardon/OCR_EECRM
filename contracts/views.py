from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Contract, ContractStatus
from .permissions import ContractPermission
from .serializers import ContractSerializer, ContractStatusSerializer

# Create your views here.

class ContractsStatusAPIView(ModelViewSet):
    serializer_class = ContractStatusSerializer
    permission_classes = (ContractPermission,)

    def get_queryset(self):
        return ContractStatus.objects.all()

class ContractsAPIView(ModelViewSet):
    """return a list of projects
    access to a specific project is enabled for author or contributors only
    updating or deleting a specific project is enabled for author only"""

    serializer_class = ContractSerializer
    permission_classes = (ContractPermission, IsAuthenticated)

    def get_queryset(self):
        return Contract.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            "message": "Project has been deleted",
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

