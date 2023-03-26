from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservation.urls')),  # table reservation system
    path('employee/', include('employee.urls')),  # employee authentication system
]
