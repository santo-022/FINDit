from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import StudentRegisterForm, StaffRegisterForm, LoginForm
from items.models import Item

def student_register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            return render(request, 'users/registration_success.html')
    else:
        form = StudentRegisterForm()

    return render(request, 'users/student_register.html', {'form': form})


def staff_register(request):
    if request.method == 'POST':
        form = StaffRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            return render(request, 'users/registration_success.html')
    else:
        form = StaffRegisterForm()

    return render(request, 'users/staff_register.html', {'form': form})

def home(request):
    items = Item.objects.filter(itemtype='LOST').order_by('-created_at')
    return render(request, 'home.html', {'items': items})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})
