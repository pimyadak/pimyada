from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 
from django.contrib.auth import views as auth_views
from .views import EmployeeListCreateAPIView


urlpatterns = [

    path('verify-employee/', views.verify_employee_view, name='verify_employee'),
    path('logout-employee/', views.logout_employee_view, name='logout_employee'),
    path('leave/', views.leave_view, name='leave'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('api/employees/', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('admin-messages/', views.admin_messages_view, name='admin_messages'),
    path('', views.home_page, name='home'),
    path('home/', views.home_page, name='home'), 
    path('about/', views.about, name='about'),
    path('index/', views.index, name='index'),
    path('person/', views.person_page, name='person'),
    path('product/', views.product_page, name='product'),
    path('form_view/', views.add_employee_view, name='form_view'),
    path('delete/<int:person_id>/', views.delete, name='delete'),
    path('blog/', views.blog, name='blog'),
    path('edit/<int:person_id>/', views.edit, name='edit'),
    path('management/', views.management_view, name='management'),
    path('product/update/<int:product_id>/<str:action>/', views.update_product_stock, name='update_stock'),
    path('management/stock/', views.stock_list_view, name='stock_list'),
    path('management/stock/add/', views.add_product, name='add_product'),
    path('management/stock/edit/<int:product_id>/', views.update_product_name, name='update_product_name'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
   path('logout/', views.logout_view, name='logout'),
   path('employee-status/',views.employee_status_view,name='employee_status',),
    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
