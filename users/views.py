from django.shortcuts import render
# from django.contrib.auth.forms import UserCreationForm
from .models import LeaveType, LeaveApplication

def home(request):
    leave_types = LeaveType.objects.all()
    return render(request, 'users/home.html',{'leave_types': leave_types} )

# def register(request):
#     form = UserCreationForm()
#     return render(request, 'users/register.html', {'form': form})

def apply(request):
    return render(request, 'users/apply.html')

def notification(request):
    return render(request, 'users/notification.html')

def profile(request):
    return render(request, 'users/profile.html')

def balance(request):
    return render(request, 'users/balance.html')


