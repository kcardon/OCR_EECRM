from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_date
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
        client_id = self.kwargs.get("client_id")
        if client_id is not None:
            queryset = Contract.objects.filter(client=client_id)
        else:
            queryset = Contract.objects.all()

        client_name = self.request.GET.get("client_name")
        if client_name is not None:
            queryset = queryset.filter(client__last_name__icontains=client_name)

        client_email = self.request.GET.get("client_email")
        if client_email is not None:
            queryset = queryset.filter(client__email__icontains=client_email)

        date_before = self.request.GET.get("date_before")
        if date_before is not None:
            date_before = parse_date(date_before)
            queryset = queryset.filter(date_created__lte=date_before)  # less or equal

        date_after = self.request.GET.get("date_after")
        if date_after is not None:
            date_after = parse_date(date_after)
            queryset = queryset.filter(date_created__gte=date_after)  # greater or equal

        amount_lte = self.request.GET.get("amount_lte")
        if amount_lte is not None:
            queryset = queryset.filter(amount__lte=amount_lte)

        amount_gte = self.request.GET.get("amount_gte")
        if amount_gte is not None:
            queryset = queryset.filter(amount__gte=amount_gte)

        return queryset

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
