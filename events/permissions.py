from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from .models import Event
from contracts.models import Contract


class EventPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return self.can_create_event(request)
        return True

    def has_object_permission(self, request, view, obj):
        return self.can_manage_event(request, obj)

    def can_manage_event(self, request, obj):
        group = self.get_user_group(request)
        if group == "Management":
            return True
        elif group == "Sales":
            event_client = obj.client
            contracts_clients = Contract.objects.filter(
                sales_contact=request.user
            ).values_list("client", flat=True)
            # La permission est donnée si le client associé à l'évènement fait partie
            # de la liste des clients des contrats attribués à l'utilisateur en cours
            return event_client in contracts_clients
        elif group == "Support":
            return obj.support_contact == request.user
        else:
            return False

    def can_create_event(self, request):
        return request.user.is_authenticated and self.get_user_group(request) in [
            "Management",
            "Sales",
        ]

    def get_user_group(self, request):
        return request.user.groups.all().values_list("name", flat=True).first()


class EventStatusPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.groups.all().values_list("name", flat=True).first()
            == "Management"
        )
