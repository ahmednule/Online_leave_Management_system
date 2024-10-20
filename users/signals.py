from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import LeaveBalance

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_leave_balance(sender, instance, created, **kwargs):
    if created:
        # Create a leave balance automatically with default values
        LeaveBalance.objects.create(user=instance, annual_leave=20, sick_leave=10, other_leave=5)
