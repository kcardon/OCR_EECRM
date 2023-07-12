from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from events.models import Event
from contracts.models import Contract


class ContractPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return self.can_create_contract(request)
        if self.get_user_group(request) == "Support":
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        return self.can_manage_contract(request, obj)

    def can_manage_contract(self, request, obj):
        group = self.get_user_group(request)
        if group == "Management":
            return True
        elif group == "Sales":
            contracts_clients = Contract.objects.filter(sales_contact=request.user)
            # La permission est donnée si le client associé à l'évènement fait partie
            # de la liste des clients des contrats attribués à l'utilisateur en cours
            return obj in contracts_clients
        else:
            return False

    def can_create_contract(self, request):
        return request.user.is_authenticated and self.get_user_group(request) in [
            "Management",
            "Sales",
        ]

    def get_user_group(self, request):
        return request.user.groups.all().values_list("name", flat=True).first()


class ContractStatusPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.groups.all().values_list("name", flat=True).first()
            == "Management"
        )
