from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import LeaveBalance, Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_records(sender, instance, created, **kwargs):
    if created:
        LeaveBalance.objects.create(user=instance, annual_leave=20, sick_leave=10, other_leave=5)
        Profile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email
        )

