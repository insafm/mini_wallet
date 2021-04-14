import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	dp = models.ImageField(blank=True)
	dp_uploaded_at = models.DateTimeField(blank=True, null=True)
	bio = models.TextField(max_length=500, blank=True)
	location = models.CharField(max_length=30, blank=True)
	website = models.CharField(max_length=255, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	phone_number = models.CharField(max_length=255, blank=True)
	gender = models.CharField(max_length=10, blank=True)
	status = models.BooleanField(default=True, blank=True)
	private_status = models.BooleanField(default=False, blank=True)
	inactive = models.BooleanField(default=False, blank=True)
	deleted = models.BooleanField(default=False, blank=True)

	user_type = models.CharField(max_length=255, blank=True, null=True)
	
	user_xid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)

	class Meta:
		permissions = (
			("member_permissions", "Member Permissions"),
			("admin_permissions", "Admin Permissions"),
		)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()