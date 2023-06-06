from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.

class UserAPIView(ModelViewSet):
    """return a list of app users"""

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()