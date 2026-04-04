from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Q
from django.shortcuts import render
from datetime import datetime
from .models import User, LeaveApplication, LeaveBalance, Notification, LeaveType, Profile, Awards, Notice, Employee_Details


class LMSAdminSite(AdminSite):
    login_template = 'admin/login.html'
    site_header = 'Leave Management — Admin'
    site_title = 'LMS Admin'
    index_title = 'Dashboard'
    index_template = 'admin/index.html'

    def index(self, request, extra_context=None):
        total_users = User.objects.filter(is_active=True).count()
        total_applications = LeaveApplication.objects.count()
        pending = LeaveApplication.objects.filter(status='Pending').count()
        approved = LeaveApplication.objects.filter(status='Approved').count()
        rejected = LeaveApplication.objects.filter(status='Rejected').count()
        cancelled = LeaveApplication.objects.filter(status='Cancelled').count()
        approval_rate = round((approved / total_applications * 100), 1) if total_applications > 0 else 0

        by_status = list(LeaveApplication.objects.values('status').annotate(count=Count('id')).order_by('-count'))
        by_type = list(LeaveApplication.objects.values('leave_type__name').annotate(count=Count('id')).order_by('-count'))

        recent_leaves = LeaveApplication.objects.select_related('user', 'leave_type').order_by('-start_date')[:10]

        context = {
            **self.each_context(request),
            'title': self.index_title,
            'total_users': total_users,
            'total_applications': total_applications,
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
            'cancelled': cancelled,
            'approval_rate': approval_rate,
            'by_status': by_status,
            'by_type': by_type,
            'recent_leaves': recent_leaves,
            'has_permission': True,
        }
        context.update(extra_context or {})
        return render(request, self.index_template, context)


admin_site = LMSAdminSite(name='lms_admin')


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    fieldsets = BaseUserAdmin.fieldsets


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'full_name', 'email', 'role', 'department', 'phone_number', 'created')
    list_filter = ('department', 'role')
    search_fields = ('user__username', 'first_name', 'last_name', 'email', 'role', 'department')
    readonly_fields = ('user',)
    list_select_related = ('user',)

    def user_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

    def created(self, obj):
        return obj.user.date_joined.strftime('%b %d, %Y')
    created.short_description = 'Joined'


class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'leave_type', 'start_date', 'end_date', 'duration_display', 'status_badge', 'submitted', 'processed_by')
    list_filter = ('status', 'leave_type', ('start_date', admin.DateFieldListFilter))
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'leave_type__name', 'message')
    readonly_fields = ('user', 'leave_type', 'start_date', 'end_date', 'message', 'approved_by', 'approved_at', 'rejected_by', 'rejected_at')
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'
    actions = ['approve_selected', 'reject_selected']
    list_per_page = 25

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return list(self.readonly_fields) + ['status', 'rejection_reason']
        return self.readonly_fields

    def has_add_permission(self, request):
        return False

    def user_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.get_full_name() or obj.user.username)
    user_link.short_description = 'Employee'

    def duration_display(self, obj):
        return f"{obj.duration} day{'s' if obj.duration != 1 else ''}"
    duration_display.short_description = 'Duration'

    def status_badge(self, obj):
        colors = {
            'Pending': 'warning',
            'Approved': 'success',
            'Rejected': 'danger',
            'Cancelled': 'secondary',
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{} px-2 py-1">{}</span>',
            color, obj.status
        )
    status_badge.short_description = 'Status'

    def submitted(self, obj):
        return obj.start_date.strftime('%b %d, %Y')
    submitted.short_description = 'Submitted'

    def processed_by(self, obj):
        if obj.status == 'Approved' and obj.approved_by:
            return f"Approved by {obj.approved_by.username}"
        if obj.status == 'Rejected' and obj.rejected_by:
            reason = f" - {obj.rejection_reason[:30]}" if obj.rejection_reason else ""
            return format_html(
                'Rejected by {}<br><small class="text-muted">{}</small>',
                obj.rejected_by.username, reason
            )
        return '<span class="text-muted">Pending review</span>'
    processed_by.short_description = 'Processed By'

    def approve_selected(self, request, queryset):
        pending = queryset.filter(status='Pending')
        count = pending.count()
        for leave in pending:
            leave.status = 'Approved'
            leave.approved_by = request.user
            leave.approved_at = datetime.now()
            leave.save()

            Notification.objects.create(
                user=leave.user,
                message=f"Your {leave.leave_type.name} leave ({leave.start_date} to {leave.end_date}) has been approved."
            )
        self.message_user(request, f'{count} leave application(s) approved.')
    approve_selected.short_description = 'Approve selected leave applications'

    def reject_selected(self, request, queryset):
        pending = queryset.filter(status='Pending')
        count = pending.count()
        reason = request.POST.get('rejection_reason', 'No reason provided.')
        for leave in pending:
            leave.status = 'Rejected'
            leave.rejection_reason = reason
            leave.rejected_by = request.user
            leave.rejected_at = datetime.now()
            leave.save()

            Notification.objects.create(
                user=leave.user,
                message=f"Your {leave.leave_type.name} leave ({leave.start_date} to {leave.end_date}) has been rejected. Reason: {reason}"
            )
        self.message_user(request, f'{count} leave application(s) rejected.')
    reject_selected.short_description = 'Reject selected leave applications'

    def response_change(self, request, obj):
        if '_approve' in request.POST:
            if obj.status == 'Pending':
                obj.status = 'Approved'
                obj.approved_by = request.user
                obj.approved_at = datetime.now()
                obj.save()
                Notification.objects.create(
                    user=obj.user,
                    message=f"Your {obj.leave_type.name} leave ({obj.start_date} to {obj.end_date}) has been approved."
                )
                self.message_user(request, 'Leave application approved.')
                return super().response_change(request, obj)
        if '_reject' in request.POST:
            if obj.status == 'Pending':
                reason = request.POST.get('rejection_reason', 'No reason provided.')
                obj.status = 'Rejected'
                obj.rejection_reason = reason
                obj.rejected_by = request.user
                obj.rejected_at = datetime.now()
                obj.save()
                Notification.objects.create(
                    user=obj.user,
                    message=f"Your {obj.leave_type.name} leave ({obj.start_date} to {obj.end_date}) has been rejected. Reason: {reason}"
                )
                self.message_user(request, 'Leave application rejected.')
        return super().response_change(request, obj)

    change_form_template = 'admin/users/leaveapplication/change_form.html'


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'annual_leave', 'sick_leave', 'other_leave', 'total')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_select_related = ('user',)

    def user_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.get_full_name() or obj.user.username)
    user_link.short_description = 'User'

    def total(self, obj):
        return obj.annual_leave + obj.sick_leave + obj.other_leave
    total.short_description = 'Total Days'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'message_truncated', 'timestamp', 'read_status')
    list_filter = ('is_read', ('timestamp', admin.DateFieldListFilter))
    search_fields = ('user__username', 'message')
    readonly_fields = ('user', 'message', 'timestamp')
    actions = ['mark_as_read', 'mark_as_unread']
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        return False

    def user_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'

    def message_truncated(self, obj):
        return obj.message[:80] + '...' if len(obj.message) > 80 else obj.message
    message_truncated.short_description = 'Message'

    def read_status(self, obj):
        if obj.is_read:
            return format_html('<span class="badge bg-success">Read</span>')
        return format_html('<span class="badge bg-warning text-dark">Unread</span>')
    read_status.short_description = 'Status'

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notification(s) marked as read.')
    mark_as_read.short_description = 'Mark selected as read'

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notification(s) marked as unread.')
    mark_as_unread.short_description = 'Mark selected as unread'


class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'application_count', 'created')
    search_fields = ('name',)
    ordering = ('name',)

    def application_count(self, obj):
        return obj.leaveapplication_set.count()
    application_count.short_description = 'Applications'

    def created(self, obj):
        return obj.id
    created.short_description = 'ID'


class AwardsAdmin(admin.ModelAdmin):
    list_display = ('award',)


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('vacancy', 'date', 'month', 'announcements')
    search_fields = ('vacancy', 'announcements')


class EmployeeDetailsAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'first_name', 'last_name', 'email', 'role', 'department')
    list_filter = ('department', 'role')
    search_fields = ('user__username', 'first_name', 'last_name', 'email')

    def user_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'


admin_site.register(User, UserAdmin)
admin_site.register(Profile, ProfileAdmin)
admin_site.register(LeaveApplication, LeaveApplicationAdmin)
admin_site.register(LeaveBalance, LeaveBalanceAdmin)
admin_site.register(Notification, NotificationAdmin)
admin_site.register(LeaveType, LeaveTypeAdmin)
admin_site.register(Awards, AwardsAdmin)
admin_site.register(Notice, NoticeAdmin)
admin_site.register(Employee_Details, EmployeeDetailsAdmin)
