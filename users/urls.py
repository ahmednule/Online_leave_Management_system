from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('apply/', views.apply, name='apply'),
    path('balance/', views.balance, name='balance'),
    path('notifications/', views.notification, name='notifications'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_contact/', views.update_contact, name='update_contact'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.user_logout, name='logout'),
    path('leaves/admin/', views.admin_view_leaves, name='admin_view_leaves'),
    path('leaves/admin/<int:leave_id>/approve/', views.admin_approve_leave, name='admin_approve_leave'),
    path('leaves/admin/<int:leave_id>/reject/', views.admin_reject_leave, name='admin_reject_leave'),
    path('leave/<int:leave_id>/', views.leave_detail, name='leave_detail'),
    path('leave/<int:leave_id>/cancel/', views.cancel_leave, name='cancel_leave'),
    path('calendar/', views.team_calendar, name='team_calendar'),
]
