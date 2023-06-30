from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from contracts.models import Contract
from events.models import Event

class EmployeePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return self.can_create_employee(request)
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return self.can_update_employee(request, obj)
        
    def can_update_employee(self, request):
        return bool(
            request.user.is_authenticated and self.get_user_group(request) in ['Management', 'Sales']
        )
    
    def can_create_employee(self,request):
        return request.user.is_authenticated and self.get_user_group(request) == 'Management'
    
    def get_user_group(self, request):
        return request.user.groups.all().values_list('name',flat=True).first()
    

class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return self.can_create_client(request)
        return True
    
    def has_object_permission(self, request, view, obj):
        if self.get_user_group(request) == 'Management':
            return True
        elif self.get_user_group(request) == 'Sales':
            # On récupère la liste des clients attribués à ce vendeur depuis la liste des contrats qu'il gère
            clients = Contract.objects.filter(sales_contact=request.user).values_list('client', flat=True)
            return obj in clients
        elif self.get_user_group(request)== 'Support':
            # On récupère la liste des clients attribués au membre support depuis la liste des évènements qu'il gère
            clients = Event.objects.filter(support_contact=request.user).values_list('client',flat=True)
            return obj in clients

    
    def can_create_client(self,request):
        return request.user.is_authenticated and self.get_user_group(request) in ['Management', 'Sales']
    
    def get_user_group(self, request):
        return request.user.groups.all().values_list('name',flat=True).first()
    

    
