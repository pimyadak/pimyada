from django.shortcuts import render, redirect
from django import forms
from .models import Employee

# คลาสฟอร์ม (ย้ายมาจาก forms.py)
class EmployeeForm(forms.ModelForm): 
    GENDER_CHOICES = [
        ('male', 'ชาย'),
        ('female', 'หญิง'),
    ]

    DEPARTMENT_CHOICES = [
        ('admin' , 'แอดมิน'),
        ('hr', 'ฝ่ายบุคคล'),
        ('it', 'ฝ่ายไอที'),
        ('sales', 'ฝ่ายขาย'),
        # เพิ่มแผนกอื่นๆ ของคุณได้ที่นี่
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Employee
        fields = '__all__'
        labels = {
            'fname': 'First Name',
            'lname': 'Last Name',
            'address': 'Address',
            'gender': 'Gender',
            'birthdate': 'Birthdate',
            'department': 'Department',
            'salary': 'Salary',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'gender': forms.Select(), # หรือ RadioSelect() ตามที่คุณต้องการ
            'birthdate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fname': forms.TextInput(attrs={'class': 'form-control'}),
            'lname': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# ฟังก์ชัน View
def form_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page') # เปลี่ยนชื่อ URL ไปยังหน้าที่ต้องการหลังบันทึก
    else:
        form = EmployeeForm()
    return render(request, 'form_view.html', {'form': form})