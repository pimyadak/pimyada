from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from .models import person, product, Post
from django.shortcuts import redirect
from .forms import Employee
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import person  
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Employee
from rest_framework import viewsets
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import ContactMessage
from django.shortcuts import render, redirect
from .models import Order  
from rest_framework.response import Response
from rest_framework import generics
from .serializers import personSerializer
from .models import person
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .models import ContactMessage # เรียกใช้ Model ข้อความ
from datetime import date
from .models import person ,Attendance
from django.core.paginator import Paginator





def contact_view(request):
    if request.method == 'POST':
        # รับค่าจากฟอร์มหน้าเว็บ (ตรวจสอบ name="..." ในไฟล์ HTML ให้ตรงกัน)
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and message:
            # บันทึกลงฐานข้อมูล
            ContactMessage.objects.create(
                name=name,
                contact=contact,
                subject=subject,
                message=message
            )
            messages.success(request, "ส่งข้อความสำเร็จเรียบร้อยแล้ว!")
            return redirect('about') # หรือเปลี่ยนไปหน้าติดต่อ
        else:
            messages.error(request, "กรุณากรอกข้อมูลให้ครบถ้วน")
            
    return render(request, 'about.html') # ชื่อไฟล์หน้าติดต่อของคุณ

# ฟังก์ชันแสดงกล่องข้อความฝั่ง Admin (admin_messages)
def admin_messages_view(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    context = {
        'messages_list': messages_list
    }
    return render(request, 'admin_messages.html', context)




def verify_employee_view(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id', '').strip().upper()  
        allowed_employee_ids = [f"EMP05{i}" for i in range(9)]  

        if emp_id in allowed_employee_ids:
            request.session['verified_employee'] = emp_id
            messages.success(request, f"ยืนยันรหัสพนักงาน {emp_id} สำเร็จ!")
        else:
            messages.error(request, "รหัสพนักงานไม่ถูกต้อง หรือไม่อยู่ในสิทธิ์ที่อนุญาต (อนุญาตเฉพาะ EMP050 - EMP058 เท่านั้น)")           
    return redirect('home')

def logout_employee_view(request):
    if 'verified_employee' in request.session:
        del request.session['verified_employee']
        messages.info(request, "ออกจากโหมดพนักงานเรียบร้อยแล้ว")
    return redirect('home')


def edit_person_view(request, person_id):
    # ป้องกันไม่ให้คนที่ไม่ใช่แอดมินเข้ามาแก้ไข
    if not request.user.is_staff:
        return redirect('person')

    
def leave_view(request):
    all_employee = person.objects.all()
    return render(request, 'leave.html', {'all_employee': all_employee})


def attendance_view(request):
    all_employee = person.objects.all()
    return render(request, 'attendance.html', {'all_employee': all_employee})


class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = person.objects.all().order_by('id')
    serializer_class = personSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'api_table.html'
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        if request.accepted_renderer.format == 'html':
            return Response({'employees': serializer.data}, template_name=self.template_name)
            
        return super().get(request, *args, **kwargs)

    
# หน้ากรอกข้อมูลสั่งซื้อของลูกค้า
def checkout_view(request):
    product_name = request.GET.get('product', 'สินค้าทั่วไป')
    price = request.GET.get('price', '0')
    
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment = request.POST.get('payment')
        
        # บันทึกข้อมูลลงฐานข้อมูล Order ทันที
        Order.objects.create(
            product_name=product_name,
            price=price,
            fullname=fullname,
            phone=phone,
            address=address,
            payment=payment
        )
        
        # บันทึกเสร็จแล้วพาพุ่งไปหน้าดูรายการของพนักงานได้เลย
        return redirect('admin_orders')
        
    context = {
        'product_name': product_name,
        'price': price,
    }
    return render(request, 'checkout.html', context)

   
# หน้าสำหรับพนักงาน/แอดมิน ดูรายการสั่งซื้อสินค้าของลูกค้า
def admin_orders(request):
    orders_list = Order.objects.all().order_by('-created_at') # ดึงรายการล่าสุดขึ้นก่อน
    return render(request, 'admin_orders.html', {'orders_list': orders_list})

def checkout_view(request):
    product_name = request.GET.get('product', 'สินค้าทั่วไป')
    price = request.GET.get('price', '0')
    
    context = {
        'product_name': product_name,
        'price': price
    }
    return render(request, 'checkout.html', context)

def about(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and message:
            # บันทึกลงฐานข้อมูลจริง
            ContactMessage.objects.create(
                name=name,
                contact=contact,
                subject=subject,
                message=message
            )
            messages.success(request, "ส่งข้อความสอบถามสำเร็จเรียบร้อยแล้วค่ะ 🌸")
            return redirect('about')  # ใช้ redirect เพื่อรีเฟรชหน้าและเคลียร์ฟอร์ม
        else:
            messages.error(request, "กรุณากรอกข้อมูลให้ครบถ้วน")
            
    return render(request, 'about.html')

def admin_messages(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    context = {
        'messages_list': messages_list
    }
    return render(request, 'admin_messages.html', context)

def employee_status_view(request):
  query = request.GET.get('q', '')

  if query:
    # ค้นหาจากชื่อหรือนามสกุล
    employees = person.objects.filter(
        Q(fname__icontains=query) | Q(lname__icontains=query)
    )
  else:
    # ดึงข้อมูลพนักงานทั้งหมดจากตาราง person มาแสดง
    employees = person.objects.all()

  context = {
      'employees': employees,
      'query': query,
  }
  return render(request, 'employee_status.html', context)


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        product.objects.create(name=name, stock=0)
    return redirect('stock_list') 

def person_page(request):
    today = date.today()
    
    # 1. ดึงรายชื่อพนักงานทั้งหมด (เรียงตาม id เพื่อป้องกัน Warning ของ Paginator)
    all_employee = person.objects.all().order_by('id')
    
    # 2. ดึงไอดีพนักงานที่เช็คอินแล้วในวันนี้
    checked_in_today = Attendance.objects.filter(
        timestamp__date=today
    ).values_list('employee_id', flat=True)
    
    # พิมพ์ตรวจสอบใน Terminal ว่ามีข้อมูลเด้งขึ้นมาไหม
    print("🚀 [CHECKED IN TODAY IDs]:", list(checked_in_today))

    # 3. ระบบ Pagination เดิมของคุณ
    paginator = Paginator(all_employee, 4) # หรือจำนวนรายการต่อหน้าของคุณ
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'all_employee': page_obj,          # ส่งค่าแบบแบ่งหน้า
        'checked_in_today': checked_in_today, # ส่งรายการไอดีที่เช็คอินแล้ว
    }
    return render(request, 'person.html', context)

def blog(request):
    posts = Post.objects.all()  
    return render(request, 'blog.html', {'posts': posts})

def index(request):
    all_employee =  Employee.objects.all()
    return render(request,'index.html' ,{"all_employee" : all_employee})

def about(request):
    return render(request,"about.html")

def home_page(request):
    return render(request,"home.html")

def product_page(request):
    return render(request,"product.html")

def contact_page(request):
    return render(request,"contact.html")


def delete(request, person_id):
    p = get_object_or_404(person, pk=person_id)   
    p.delete()
    return redirect('person')

def form_view(request):
    if request.method == 'POST':
       
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        age = request.POST.get('age')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        birthdate = request.POST.get('birthdate')   
        department = request.POST.get('department')    
        salary = request.POST.get('salary')    
        
        # บันทึกลงฐานข้อมูล
        Employee.objects.create(
            fname=fname,
            lname=lname,
            age=age,
            address=address,
            gender=gender,
            birthdate=birthdate,
            department=department,
            salary=salary,
        )
        return redirect('form_view') 
        
    return render(request, 'form_view.html')

def edit(request, person_id):
    p = get_object_or_404(person, id=person_id)
    error_message = None

    if request.method == 'POST':
        birthdate_input = request.POST.get('birthdate')
        
        # ตรวจสอบความยาวของปี
        if birthdate_input and len(birthdate_input.split('-')[0]) > 4:
            error_message = 'รูปแบบปีผิดพลาด โปรดกรอกปี ค.ศ. 4 หลัก'
        else:
            # บันทึกข้อมูลเฉพาะเมื่อไม่ติด Error
            p.fname = request.POST.get('fname')
            p.lname = request.POST.get('lname')
            p.age = request.POST.get('age')
            p.address = request.POST.get('address')
            p.gender = request.POST.get('gender')
            p.birthdate = birthdate_input
            p.department = request.POST.get('department')
            p.salary = request.POST.get('salary')
            
            if request.FILES.get('pics'):
                p.pics = request.FILES.get('pics')
            
            p.save()
            return redirect('person')

    return render(request, 'edit.html', {
        'person': p,
        'error': error_message
    })

def management_view(request):
    # ดึงสินค้าทั้งหมดมา
    products = product.objects.all()
    # ดึงค่าสถิติเดิม (ถ้ามี)
    total_persons = person.objects.count()
    total_products = products.count()
    total_stock = products.aggregate(Sum('stock'))['stock__sum'] or 0
    
    context = {
        'products': products,
        'total_persons': total_persons,
        'total_products': total_products,
        'total_stock': total_stock,
    }
    return render(request, 'management.html', context)

def product_page(request):
    products = product.objects.all()
    return render(request, 'product.html', {'products': products})

def stock_list_view(request):
    products = product.objects.all()
    return render(request, 'stock_list.html', {'products': products})
    

def update_stock(request, product_id):
    product = get_object_or_404(product, pk=product_id)
    if request.method == 'POST':
        # รับค่าจำนวนใหม่จากฟอร์ม
        new_stock = request.POST.get('stock')
        product.stock = new_stock
        product.save()
        return redirect('product') # กลับไปหน้าแสดงสินค้า
    return render(request, 'update_stock.html', {'product': product})

def update_product_stock(request, product_id, action):
    print(f"กำลังอัปเดตสินค้า ID: {product_id}, การกระทำ: {action}") # เช็คใน Terminal ว่ามีข้อความนี้ขึ้นไหม
    item = get_object_or_404(product, pk=product_id)
    
    if action == 'increase':
        item.stock += 1
    elif action == 'decrease' and item.stock > 0:
        item.stock -= 1
        
    item.save()
    return redirect('stock_list')

def update_product_name(request, product_id):
    if request.method == 'POST':
        item = get_object_or_404(product, pk=product_id)
        item.name = request.POST.get('new_name')
        item.save()
    return redirect('stock_list')

# จากเดิมที่ใช้ Employee
def add_employee_view(request):
    if request.method == 'POST':
        
        # รับค่าจากฟอร์มให้ครบทุกช่อง
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        age = request.POST.get('age')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        birthdate = request.POST.get('birthdate')
        department = request.POST.get('department')
        salary = request.POST.get('salary')
        pics = request.FILES.get('image') # ชื่อ name ใน <input type="file">

        if birthdate and len(birthdate.split('-')[0]) > 4:
            return render(request, 'person.html', {
                'error': 'รูปแบบปีผิดพลาด โปรดกรอกปี ค.ศ. 4 หลัก'
            })

        # บันทึกลงฐานข้อมูล
        person.objects.create(
            fname=f"{fname} ",
            lname=lname,
            age=27, # ถ้ามีฟิลด์อายุให้รับค่าจากฟอร์มด้วย
            address=address,
            gender=gender,
            birthdate=birthdate,
            department=department,
            salary=salary,
            pics=pics,
        )
        return redirect('person')

    return render(request, 'form_view.html')

def login_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        
        user = authenticate(request, username=user_name, password=pass_word)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง'})
            

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word1 = request.POST.get('password1')
        pass_word2 = request.POST.get('password2')
        
        # ตรวจสอบความยาวรหัสผ่านอย่างน้อย 6 ตัวอักษร
        if len(pass_word1) < 6:
            return render(request, 'register.html', {'error': 'รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษรขึ้นไป'})
            
        if pass_word1 == pass_word2:
            if not User.objects.filter(username=user_name).exists():
                User.objects.create_user(username=user_name, password=pass_word1)
                
                return redirect('login')
            else:
                return render(request, 'register.html', {'error': 'ชื่อผู้ใช้นี้มีคนใช้แล้ว'})
        else:
            return render(request, 'register.html', {'error': 'รหัสผ่านไม่ตรงกัน'})
            
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')


    

        