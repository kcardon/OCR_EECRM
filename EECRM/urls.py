"""
URL configuration for EECRM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from contracts.views import ContractsAPIView, ContractsStatusAPIView
from persons.views import EmployeeAPIView, EmployeeSignupAPIView, EmployeeLoginAPIView, GroupAPIView, ClientAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", EmployeeLoginAPIView.as_view(), name = "login"),
    
]

# Création du routeur
router_root = routers.DefaultRouter()
# Déclaration des urls du routeur

router_root.register("employees", EmployeeAPIView, basename="employees")
router_root.register("signup", EmployeeSignupAPIView, basename = "signup")
router_root.register("groups", GroupAPIView, basename= "groups" )
router_root.register("clients", ClientAPIView, basename = "clients")
router_root.register("contracts_status", ContractsStatusAPIView, basename = "contracts_status")
router_root.register("contracts", ContractsAPIView, basename = "contracts")
urlpatterns += [path("", include(router_root.urls))]


router_root = routers.DefaultRouter()

router_root.register("contracts", ContractsAPIView, basename="contracts")

urlpatterns += [path("", include(router_root.urls))]
