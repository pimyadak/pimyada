import uuid
from django.db import models
from rest_framework import serializers


class Attendance(models.Model):
    employee = models.ForeignKey('person', on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=50)  # ใช้เก็บสถานะ เช่น 'เข้างาน' หรือ 'ออกงาน'
    timestamp = models.DateTimeField(auto_now_add=True)  # บันทึกวันและเวลาแบบ Real-time

    def __str__(self):
        return f"{self.employee} - {self.action} ({self.timestamp})"

class Order(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    payment = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"คำสั่งซื้อ {self.product_name} โดย {self.fullname}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100) 
    subject = models.CharField(max_length=200) 
    message = models.TextField()              
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Employee(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True) 
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):  
        return self.title

class person(models.Model):
    emp_id = models.CharField(
      max_length=20, unique=True, blank=True, null=True, verbose_name='รหัสพนักงาน'
  )
    
    fname = models.CharField(max_length=100) 
    lname = models.CharField(max_length=100) 
    age = models.IntegerField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # ใน models.py
    pics = models.ImageField(upload_to='images/', blank=True, null=True)
    check_in_time = models.DateTimeField(blank=True, null=True)  # เวลาเข้างาน (Check-in)
    check_out_time = models.DateTimeField(blank=True, null=True)  # เวลาออกงาน (Check-out)
    is_online = models.BooleanField(default=False)  

    def save(self, *args, **kwargs):
      # 1. บันทึกข้อมูลลงฐานข้อมูลก่อน 1 ครั้ง เพื่อให้ระบบรันและสร้าง id ประจำตัวขึ้นมาก่อน
      super().save(*args, **kwargs)

      # 2. ถ้ายังไม่มี emp_id ให้สร้างจาก id ของตัวเองทันที (รับรองว่าไม่ซ้ำและไม่เป็น None แน่นอน)
      if not self.emp_id:
        self.emp_id = f'EMP{self.id:03d}'
        super().save(update_fields=['emp_id'])
    def __str__(self):
        return f'{self.emp_id} - {self.fname} {self.lname}'
    
class product(models.Model):
    name = models.CharField(max_length=200)
    stock = models.IntegerField(default=0) 

    def __str__(self):
        return f"{self.fname} {self.lname}"
    
    
    

