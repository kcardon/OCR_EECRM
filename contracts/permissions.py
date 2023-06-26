from rest_framework.permissions import BasePermission


class ContractPermission(BasePermission):
    def has_permission(self, request, view):
        
        return True