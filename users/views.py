from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash, logout, login
from django.contrib import messages
from django.urls import reverse
from django.http import Http404, HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Avg
from datetime import datetime
from .models import LeaveType, LeaveApplication, Notification, LeaveBalance, Profile, Notice, Awards
from .forms import ProfileForm, ContactForm

ITEMS_PER_PAGE = 10

def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'registration/login.html', {'form': form})

@login_required
def home(request):
    leave_applications = LeaveApplication.objects.filter(user=request.user).order_by('-start_date')
    notice = Notice.objects.all()
    awards = Awards.objects.all()
    pending_count = leave_applications.filter(status='Pending').count()
    approved_count = leave_applications.filter(status='Approved').count()

    return render(request, 'users/home.html', {
        'notice': notice,
        'awards': awards,
        'leave_applications': leave_applications[:5],
        'pending_count': pending_count,
        'approved_count': approved_count,
    })

@login_required
def apply(request):
    if request.method == 'POST':
        leave_type_name = request.POST.get('leave_type')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        message = request.POST.get('message')

        existing = LeaveApplication.objects.filter(
            user=request.user,
            status='Pending',
            start_date__lte=start_date,
            end_date__gte=start_date
        ).exists()
        if existing:
            messages.error(request, 'You already have a pending leave application that overlaps with these dates.')
            leave_types = LeaveType.objects.all()
            return render(request, 'users/apply.html', {'leave_types': leave_types})

        leave_type = get_object_or_404(LeaveType, name=leave_type_name)

        LeaveApplication.objects.create(
            user=request.user,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            message=message,
            status='Pending'
        )

        messages.success(request, 'Leave application submitted successfully.')
        return redirect('home')

    leave_types = LeaveType.objects.all()
    return render(request, 'users/apply.html', {'leave_types': leave_types})

@login_required
def notification(request):
    leave_applications = LeaveApplication.objects.filter(user=request.user).order_by('-start_date')

    status_filter = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if status_filter:
        leave_applications = leave_applications.filter(status=status_filter)
    if date_from:
        leave_applications = leave_applications.filter(start_date__gte=date_from)
    if date_to:
        leave_applications = leave_applications.filter(end_date__lte=date_to)

    paginator = Paginator(leave_applications, ITEMS_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        leave_applications = paginator.page(page)
    except PageNotAnInteger:
        leave_applications = paginator.page(1)
    except EmptyPage:
        leave_applications = paginator.page(paginator.num_pages)

    return render(request, 'users/notification.html', {
        'user': request.user,
        'leave_applications': leave_applications,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
    })

@login_required
def leave_detail(request, leave_id):
    leave = get_object_or_404(LeaveApplication, id=leave_id)
    if leave.user != request.user and not request.user.is_superuser:
        raise Http404('Leave application not found.')
    return render(request, 'users/leave_detail.html', {'leave': leave})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

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
    leave_balance, created = LeaveBalance.objects.get_or_create(user=request.user)
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
def cancel_leave(request, leave_id):
    leave_application = get_object_or_404(LeaveApplication, id=leave_id)
    if leave_application.user != request.user:
        raise Http404('You do not have permission to cancel this leave.')
    if leave_application.status != 'Pending':
        messages.error(request, 'Only pending leave applications can be cancelled.')
        return redirect('notifications')

    leave_application.status = 'Cancelled'
    leave_application.save()
    messages.success(request, 'Leave application cancelled successfully.')
    return redirect('notifications')

@login_required
def admin_approve_leave(request, leave_id):
    if not request.user.is_superuser:
        raise Http404('You do not have permission to perform this action.')

    leave_application = get_object_or_404(LeaveApplication, id=leave_id)
    if leave_application.status != 'Pending':
        messages.error(request, 'This leave application has already been processed.')
        return redirect(reverse('admin_view_leaves'))

    duration = leave_application.duration
    leave_type_name = leave_application.leave_type.name.lower()

    leave_balance, _ = LeaveBalance.objects.get_or_create(user=leave_application.user)

    if 'annual' in leave_type_name:
        leave_balance.annual_leave = max(0, leave_balance.annual_leave - duration)
    elif 'sick' in leave_type_name:
        leave_balance.sick_leave = max(0, leave_balance.sick_leave - duration)
    else:
        leave_balance.other_leave = max(0, leave_balance.other_leave - duration)
    leave_balance.save()

    leave_application.status = 'Approved'
    leave_application.approved_by = request.user
    leave_application.approved_at = datetime.now()
    leave_application.save()

    Notification.objects.create(
        user=leave_application.user,
        message=f'Your leave application for {leave_application.leave_type.name} from {leave_application.start_date} to {leave_application.end_date} has been approved.'
    )

    try:
        send_mail(
            subject='Leave Application Approved',
            message=(
                f'Dear {leave_application.user.get_full_name() or leave_application.user.username},\n\n'
                f'Your leave application for {leave_application.leave_type.name} '
                f'from {leave_application.start_date} to {leave_application.end_date} '
                f'({duration} day(s)) has been approved.\n\n'
                f'Best regards,\nLeave Management System'
            ),
            from_email='noreply@leavemanagement.local',
            recipient_list=[leave_application.user.email],
            fail_silently=True,
        )
    except Exception:
        pass

    messages.success(request, 'Leave application approved successfully.')
    return redirect(reverse('admin_view_leaves'))

@login_required
def admin_reject_leave(request, leave_id):
    if not request.user.is_superuser:
        raise Http404('You do not have permission to perform this action.')

    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect(reverse('admin_view_leaves'))

    leave_application = get_object_or_404(LeaveApplication, id=leave_id)
    if leave_application.status != 'Pending':
        messages.error(request, 'This leave application has already been processed.')
        return redirect(reverse('admin_view_leaves'))

    leave_application.status = 'Rejected'
    leave_application.rejection_reason = rejection_reason
    leave_application.rejected_by = request.user
    leave_application.rejected_at = datetime.now()
    leave_application.save()

    Notification.objects.create(
        user=leave_application.user,
        message=f'Your leave application for {leave_application.leave_type.name} from {leave_application.start_date} to {leave_application.end_date} has been rejected.'
    )

    try:
        reason_text = f'\n\nReason: {rejection_reason}' if rejection_reason else ''
        send_mail(
            subject='Leave Application Rejected',
            message=(
                f'Dear {leave_application.user.get_full_name() or leave_application.user.username},\n\n'
                f'Your leave application for {leave_application.leave_type.name} '
                f'from {leave_application.start_date} to {leave_application.end_date} '
                f'has been rejected.{reason_text}\n\n'
                f'Best regards,\nLeave Management System'
            ),
            from_email='noreply@leavemanagement.local',
            recipient_list=[leave_application.user.email],
            fail_silently=True,
        )
    except Exception:
        pass

    messages.success(request, 'Leave application rejected.')
    return redirect(reverse('admin_view_leaves'))

@login_required
def admin_view_leaves(request):
    if not request.user.is_superuser:
        raise Http404('You do not have permission to view this page.')

    leave_applications = LeaveApplication.objects.all().order_by('-start_date')

    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if status_filter:
        leave_applications = leave_applications.filter(status=status_filter)
    if search_query:
        leave_applications = leave_applications.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(leave_type__name__icontains=search_query)
        )
    if date_from:
        leave_applications = leave_applications.filter(start_date__gte=date_from)
    if date_to:
        leave_applications = leave_applications.filter(end_date__lte=date_to)

    paginator = Paginator(leave_applications, ITEMS_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        leave_applications = paginator.page(page)
    except PageNotAnInteger:
        leave_applications = paginator.page(1)
    except EmptyPage:
        leave_applications = paginator.page(paginator.num_pages)

    return render(request, 'users/admin_view_leaves.html', {
        'leave_applications': leave_applications,
        'status_filter': status_filter,
        'search_query': search_query,
        'date_from': date_from,
        'date_to': date_to,
    })

@login_required
def team_calendar(request):
    if not request.user.is_superuser:
        raise Http404('Admin access required.')

    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))

    if month < 1:
        month, year = 12, year - 1
    if month > 12:
        month, year = 1, year + 1

    approved_leaves = LeaveApplication.objects.filter(
        status='Approved',
        start_date__year=year,
        start_date__month=month
    ).select_related('user', 'leave_type')

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    import calendar
    month_name = calendar.month_name[month]

    return render(request, 'users/team_calendar.html', {
        'approved_leaves': approved_leaves,
        'year': year,
        'month': month,
        'month_name': month_name,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    })



@login_required
def admin_analytics(request):
    if not request.user.is_superuser:
        raise Http404('Admin access required.')
    total = LeaveApplication.objects.count()
    approved = LeaveApplication.objects.filter(status='Approved').count()
    rejected = LeaveApplication.objects.filter(status='Rejected').count()
    pending = LeaveApplication.objects.filter(status='Pending').count()
    cancelled = LeaveApplication.objects.filter(status='Cancelled').count()
    approval_rate = round((approved / total * 100), 1) if total > 0 else 0
    rejection_rate = round((rejected / total * 100), 1) if total > 0 else 0
    by_type = list(LeaveApplication.objects.values('leave_type__name').annotate(count=Count('id')).order_by('-count'))
    by_department = list(Profile.objects.values('department').annotate(count=Count('user')).order_by('-count')[:10])
    by_status = list(LeaveApplication.objects.values('status').annotate(count=Count('id')).order_by('-count'))
    approved_this_month = LeaveApplication.objects.filter(status='Approved', start_date__month=datetime.now().month, start_date__year=datetime.now().year).count()
    pending_this_month = LeaveApplication.objects.filter(status='Pending', start_date__month=datetime.now().month, start_date__year=datetime.now().year).count()
    return render(request, 'users/admin_analytics.html', {
        'total': total, 'approved': approved, 'rejected': rejected,
        'pending': pending, 'cancelled': cancelled,
        'approval_rate': approval_rate, 'rejection_rate': rejection_rate,
        'by_type': by_type, 'by_department': by_department,
        'by_status': by_status,
        'approved_this_month': approved_this_month,
        'pending_this_month': pending_this_month,
    })

@login_required
def manage_leave_types(request):
    if not request.user.is_superuser:
        raise Http404('Admin access required.')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            name = request.POST.get('name', '').strip()
            if name and not LeaveType.objects.filter(name__iexact=name).exists():
                LeaveType.objects.create(name=name)
                messages.success(request, f'Leave type added successfully.')
            else:
                messages.error(request, 'Leave type already exists or name is invalid.')
        elif action == 'delete':
            lt_id = request.POST.get('leave_type_id')
            lt = get_object_or_404(LeaveType, id=lt_id)
            lt.delete()
            messages.success(request, 'Leave type deleted.')
        elif action == 'edit':
            lt_id = request.POST.get('leave_type_id')
            new_name = request.POST.get('new_name', '').strip()
            lt = get_object_or_404(LeaveType, id=lt_id)
            lt.name = new_name
            lt.save()
            messages.success(request, 'Leave type updated.')
    leave_types = LeaveType.objects.all().order_by('name')
    return render(request, 'users/leave_types.html', {'leave_types': leave_types})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
                email=request.POST.get('email', ''),
                role=request.POST.get('role', ''),
                department=request.POST.get('department', '')
            )
            LeaveBalance.objects.create(user=user, annual_leave=20, sick_leave=10, other_leave=5)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome aboard.')
            return redirect('home')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
