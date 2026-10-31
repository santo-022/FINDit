
from django.shortcuts import render
from .forms import StudentRegisterForm, StaffRegisterForm


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
