from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employeeapp.views import EmployeeViewSet , employee_table_view

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('table/', employee_table_view, name='employee_table'),
    path('', include(router.urls)),
]