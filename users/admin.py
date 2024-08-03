from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, LeaveApplication, LeaveBalance, Notification, LeaveType, Profile

class UserAdmin(BaseUserAdmin):
    # Add any customizations for the User admin interface here
    pass

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'role', 'department')

class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'start_date', 'end_date', 'status')

class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'annual_leave', 'sick_leave', 'other_leave')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp', 'is_read')

class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Register the models
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(LeaveApplication, LeaveApplicationAdmin)
admin.site.register(LeaveBalance, LeaveBalanceAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(LeaveType, LeaveTypeAdmin)
