import uuid
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.models import F
import datetime

from .models import MasterWallet, WalletTransaction
from ins_user.models import Profile

class RegisterSerializer(serializers.Serializer):

	customer_xid = serializers.UUIDField(format='hex_verbose')

	def __init__(self, *args, **kwargs):
		super(RegisterSerializer, self).__init__(*args, **kwargs) # call the super() 
		for field in self.fields: # iterate over the serializer fields
			self.fields[field].error_messages['required'] = 'Missing data for required field.' # set the custom error message

	# def validate(self, attrs):
	# 	return attrs

	def create(self, data, extra_user_data):
		resp = {}

		check = Profile.objects.filter(user_xid=data['customer_xid']).exists()
		if check:
			resp["error"] = "Customer xid already exists."
			return resp

		user = User.objects.create(
			username=extra_user_data['username'],
			email=extra_user_data['email'],
			first_name=extra_user_data['first_name'],
			last_name=extra_user_data['last_name']
		)

		user.set_password(extra_user_data['password'])
		user.save()

		user.refresh_from_db()
		user.profile.user_xid = data['customer_xid']
		user.save()

		# Init wallet
		MasterWallet(user=user.profile, status=0, balance=0).save()
		
		# Create token for your user.
		token, created = Token.objects.get_or_create(user=user)
		resp["token"] = token.key
		
		return resp


class WalletTransactionSerializer(serializers.Serializer):

	amount = serializers.FloatField()
	reference_id = serializers.UUIDField(format='hex_verbose', validators=[UniqueValidator(queryset=WalletTransaction.objects.all())])

	def __init__(self, *args, **kwargs):
		super(WalletTransactionSerializer, self).__init__(*args, **kwargs) # call the super()
		category = self.context.get('view').kwargs.get('category')
		self.fields['reference_id'].validators = [UniqueValidator(queryset=WalletTransaction.objects.filter(category=category))]

	# def validate(self, attrs):
	# 	return attrs

	def create(self, data, user, category):

		amount = float(data['amount'])
		balance = amount
		credit_status = 1
		resp_key = category[:-1]
		past_form = "deposited"
		if category == 'withdrawals':
			balance = amount * -1
			credit_status = 0
			past_form = "withdrawn"

		resp = {}
		# Check wallet enabled
		enabled = MasterWallet.objects.filter(user=user, status=1).first()
		if not enabled:
			resp['error'] = "Wallet not enabled."
			return resp

		# Check balance for withdrawal
		if category == 'withdrawals' and enabled.balance < amount:
			resp['error'] = "Not enough balance in wallet."
			return resp

		# Create transaction
		transaction = WalletTransaction.objects.create(
			user = user,
			amount = amount,
			balance = balance,
			credit_status = credit_status,
			reference_id = data['reference_id'],
			associated_user = user,
			status = 1,
			created = datetime.datetime.now(),
			category = category,
		)

		MasterWallet.objects.filter(user=user).update(balance=F('balance') + balance)
		
		resp[resp_key] = {}
		resp[resp_key]['id'] = transaction.pk
		resp[resp_key][past_form+'_by'] = transaction.user.user_xid
		resp[resp_key][past_form+'_at'] = transaction.created
		resp[resp_key]['status'] = "success"
		resp[resp_key]['amount'] = transaction.amount
		resp[resp_key]['reference_id'] = transaction.reference_id
		
		return resp


class MasterWalletSerializer(serializers.Serializer):
	
	def get_balance(self, data, user):
		wallet_obj = MasterWallet.objects.filter(user=user, status=1).first()
		return_data = {}
		if wallet_obj:
			return_data['wallet'] = {}
			return_data['wallet']['id'] = wallet_obj.pk
			return_data['wallet']['owned_by'] = user.user_xid
			return_data['wallet']['status'] = "enabled" if wallet_obj.status == 1 else "disabled"
			return_data['wallet']['enabled_at'] = wallet_obj.enabled_at
			return_data['wallet']['balance'] = wallet_obj.balance
		else:
			return_data['error'] = "Disabled"

		return return_data

	def enable_wallet(self, data, user):
		wallet_obj = MasterWallet.objects.filter(user=user, status=0).first()
		return_data = {}
		if wallet_obj:

			wallet_obj.status = 1
			wallet_obj.enabled_at = datetime.datetime.now()
			wallet_obj.save()

			return_data['wallet'] = {}
			return_data['wallet']['id'] = wallet_obj.pk
			return_data['wallet']['owned_by'] = user.user_xid
			return_data['wallet']['status'] = "enabled" if wallet_obj.status == 1 else "disabled"
			return_data['wallet']['enabled_at'] = wallet_obj.enabled_at
			return_data['wallet']['balance'] = wallet_obj.balance
		else:
			return_data['error'] = "Already enabled"

		return return_data

	def disable_wallet(self, data, user):
		wallet_obj = MasterWallet.objects.filter(user=user, status=1).first()
		return_data = {}
		if wallet_obj:
			wallet_obj.status = 0
			wallet_obj.disabled_at = datetime.datetime.now()
			wallet_obj.save()

			return_data['wallet'] = {}
			return_data['wallet']['id'] = wallet_obj.pk
			return_data['wallet']['owned_by'] = user.user_xid
			return_data['wallet']['status'] = "enabled" if wallet_obj.status == 1 else "disabled"
			return_data['wallet']['disabled_at'] = wallet_obj.disabled_at
			return_data['wallet']['balance'] = wallet_obj.balance
		else:
			return_data['error'] = "Already Disabled"

		return return_data