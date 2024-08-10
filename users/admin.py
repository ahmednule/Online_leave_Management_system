from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, LeaveApplication, LeaveBalance, Notification, LeaveType, Profile

class UserAdmin(BaseUserAdmin):
    # Customize User admin interface if needed
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ()
    list_filter = ('is_staff', 'is_superuser')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'role', 'department')
    search_fields = ('user__username', 'first_name', 'last_name', 'email')

class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'leave_type', 'user')
    search_fields = ('user__username', 'leave_type__name', 'message')
    ordering = ('-start_date',)
    
    # Add actions to approve and reject leave applications
    actions = ['approve_leaves', 'reject_leaves']

    def approve_leaves(self, request, queryset):
        updated = queryset.update(status='Approved')
        self.message_user(request, f'{updated} leave applications have been approved.')
    approve_leaves.short_description = 'Approve selected leave applications'

    def reject_leaves(self, request, queryset):
        updated = queryset.update(status='Rejected')
        self.message_user(request, f'{updated} leave applications have been rejected.')
    reject_leaves.short_description = 'Reject selected leave applications'

class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'annual_leave', 'sick_leave', 'other_leave')
    search_fields = ('user__username',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp', 'is_read')
    list_filter = ('is_read', 'user')
    search_fields = ('user__username', 'message')
    ordering = ('-timestamp',)

class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register the models
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(LeaveApplication, LeaveApplicationAdmin)
admin.site.register(LeaveBalance, LeaveBalanceAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(LeaveType, LeaveTypeAdmin)
