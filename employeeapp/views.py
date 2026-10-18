from django.shortcuts import render
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

def employee_table_view(request):
    employees = Employee.objects.all()
    return render(request, 'employeeapp/employee_table.html', {'employees': employees})
# Create your views here.
