from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib import messages
from django.urls import reverse
from django.http import Http404
from .models import LeaveType, LeaveApplication, Notification, LeaveBalance, Profile
from .forms import ProfileForm, ContactForm

@login_required
def home(request):
    # Fetch recent leave applications for the current user
    leave_applications = LeaveApplication.objects.filter(user=request.user).order_by('-start_date')

    return render(request, 'users/home.html', {
        'user': request.user,
        'leave_applications': leave_applications
    })

@login_required
def apply(request):
    if request.method == 'POST':
        leave_type_name = request.POST.get('leave_type')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        message = request.POST.get('message')

        # Fetch the LeaveType instance based on the name
        leave_type = get_object_or_404(LeaveType, name=leave_type_name)

        # Save the leave application to the database
        LeaveApplication.objects.create(
            user=request.user,
            leave_type=leave_type,  # Use the LeaveType instance here
            start_date=start_date,
            end_date=end_date,
            message=message,
            status='Pending'  # Assuming the default status is 'Pending'
        )

        messages.success(request, 'Leave application submitted successfully.')
        return redirect('home')

    leave_types = LeaveType.objects.all()
    return render(request, 'users/apply.html', {'leave_types': leave_types})

@login_required
def notification(request):
    # notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    leave_applications = LeaveApplication.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'users/notification.html', {
        'user': request.user,
        'leave_applications': leave_applications
    })


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Handle profile form submission
    if request.method == 'POST' and 'update_profile' in request.POST:
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect(reverse('profile'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = ProfileForm(instance=profile)

    # Handle contact form submission
    if request.method == 'POST' and 'update_contact' in request.POST:
        contact_form = ContactForm(request.POST, instance=profile)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Contact information updated successfully.')
            return redirect(reverse('profile'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        contact_form = ContactForm(instance=profile)

    return render(request, 'users/profile.html', {
        'user': request.user,
        'profile': profile,
        'profile_form': profile_form,
        'contact_form': contact_form
    })

@login_required
def balance(request):
    try:
        leave_balance = LeaveBalance.objects.get(user=request.user)
    except LeaveBalance.DoesNotExist:
        raise Http404("Leave balance does not exist for this user.")
    
    recent_leaves = LeaveApplication.objects.filter(user=request.user).order_by('-start_date')[:5]
    
    context = {
        'leave_balance': leave_balance,
        'recent_leaves': recent_leaves,
    }
    return render(request, 'users/balance.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse('profile'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/update_profile.html', {'form': form})

@login_required
def update_contact(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact information updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm(instance=profile)
    return render(request, 'users/update_profile.html', {'form': form})

@login_required
def admin_approve_leave(request, leave_id):
    if not request.user.is_superuser:
        raise Http404("You do not have permission to perform this action.")
    
    leave_application = get_object_or_404(LeaveApplication, id=leave_id)
    leave_application.status = LeaveApplication.APPROVED
    leave_application.save()
    
    messages.success(request, 'Leave application approved successfully.')
    return redirect(reverse('admin_view_leaves'))

@login_required
def admin_reject_leave(request, leave_id):
    if not request.user.is_superuser:
        raise Http404("You do not have permission to perform this action.")
    
    leave_application = get_object_or_404(LeaveApplication, id=leave_id)
    leave_application.status = LeaveApplication.REJECTED
    leave_application.save()
    
    messages.success(request, 'Leave application rejected successfully.')
    return redirect(reverse('admin_view_leaves'))

@login_required
def admin_view_leaves(request):
    if not request.user.is_superuser:
        raise Http404("You do not have permission to view this page.")
    
    leave_applications = LeaveApplication.objects.all().order_by('-start_date')
    return render(request, 'users/admin_view_leaves.html', {'leave_applications': leave_applications})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return render(request, 'users/logout.html')


