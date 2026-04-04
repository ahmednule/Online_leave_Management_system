from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('apply/', views.apply, name='apply'),
    path('balance/', views.balance, name='balance'),
    path('notifications/', views.notification, name='notifications'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_contact/', views.update_contact, name='update_contact'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.user_logout, name='logout'),
    path('admin/leaves/', views.admin_view_leaves, name='admin_view_leaves'),
    path('admin/leaves/<int:leave_id>/approve/', views.admin_approve_leave, name='admin_approve_leave'),
    path('admin/leaves/<int:leave_id>/reject/', views.admin_reject_leave, name='admin_reject_leave'),
]