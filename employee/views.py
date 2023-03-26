from employee.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser


# Employee register view
class EmployeeRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = RegisterSerializer
