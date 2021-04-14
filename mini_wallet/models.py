from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.postgres.fields import JSONField
import uuid

from ins_user.models import Profile

# Create your models here.
class MasterWallet(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE,default=0)
	status = models.SmallIntegerField(default=0, blank=True, null=True)
	enabled_at = models.DateTimeField(null=True, blank=True)
	disabled_at = models.DateTimeField(null=True, blank=True)
	created = models.DateTimeField(default=timezone.now)
	balance = models.DecimalField(decimal_places=15,max_digits=50)

	class Meta:
		indexes = [
			models.Index(fields=['user']),
		]
		index_together = [
			["user", "balance"],
		]

class WalletTransaction(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE,default=0)
	amount = models.DecimalField(decimal_places=15, max_digits=50)
	balance = models.DecimalField(decimal_places=15, max_digits=50)
	category = models.CharField(max_length=100)
	notes = models.CharField(max_length=100, default='', blank=True, null=True)
	credit_status = models.SmallIntegerField(default=0, blank=True)
	reference_id = models.CharField(max_length=255, blank=True)
	associated_user = models.ForeignKey(Profile, on_delete=models.CASCADE, default=0, related_name="associated_user")
	created = models.DateTimeField(default=timezone.now)
	status = models.SmallIntegerField(default=0, blank=True, null=True)
	extra = JSONField(default=dict, blank=True, null=True)

	class Meta:
		indexes = [
			models.Index(fields=['user']),
		]