from django.shortcuts import render, get_object_or_404
from django.http import Http404

from django.utils.dateparse import parse_date
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Contract, ContractStatus
from .permissions import ContractPermission
from .serializers import ContractSerializer, ContractStatusSerializer
from .filters import ContractFilter
from events.models import Event

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
        client_id = self.kwargs.get("client_id")
        if client_id is not None:
            queryset = Contract.objects.filter(client=client_id)
        else:
            group = self.get_user_group(self.request)
            if group == "Management":
                queryset = Contract.objects.all()
            elif group == "Sales":
                queryset = Contract.objects.filter(sales_contact=self.request.user)

        filtered_queryset = ContractFilter(self.request.GET, queryset=queryset)
        return filtered_queryset.qs

    def get_object(self):
        try:
            obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
            self.check_object_permissions(self.request, obj)
            return obj
        except Http404:
            logger.error("Contract with pk %s not found.", self.kwargs["pk"])
            return Response(
                {"error": "Contract not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_data = {
            "message": "Project has been deleted",
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    def get_user_group(self, request):
        return request.user.groups.all().values_list("name", flat=True).first()
