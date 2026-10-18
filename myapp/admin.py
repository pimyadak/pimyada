from django.contrib import admin
from .models import person  # หรือชื่อ Model ของคุณ
from .forms import EmployeeForm # นำเข้าฟอร์มที่คุณสร้างไว้

@admin.register(person)
class PersonAdmin(admin.ModelAdmin):
    form = EmployeeForm
    fields = ['fname', 'lname', 'age', 'address', 'gender', 'birthdate', 'department', 'salary' , 'pics' , 'check_in_time', 
      'check_out_time', 'is_online',]
    #เมื่อคุณสร้าง forms.py ขึ้นมา มันเป็นฟอร์มสำหรับหน้าเว็บทั่วไป (หน้า person_page
    #การใส่ form = EmployeeForm ใน admin.py จะไป "บังคับ" ให้หน้า Admin ใช้การตั้งค่า (Labels, Widgets) จาก EmployeeForm