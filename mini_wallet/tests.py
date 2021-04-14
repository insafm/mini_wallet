from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

import uuid

from django.contrib.auth.models import User
from .models import *

# Create your tests here.
class ModelTestCase(TestCase):
	"""This class defines the test suite for the bucketlist model."""

	def setUp(self):
		"""Define the test client and other test variables."""
		self.user = User.objects.create(first_name="first_name", last_name="last_name", email="insishere@mailinator.net", username="username1", password='Abc@12345')
		
		uuid_string = "ea0212d3-abd6-406f-8c67-868e814a2436"
		self.user.refresh_from_db()
		self.user.profile.user_xid = uuid.UUID(uuid_string).hex
		self.user.save()

		self.master_wallet = MasterWallet(user=self.user.profile, status=0, balance=0)
		self.wallet_transaction = WalletTransaction(user=self.user.profile, status=1, amount=100, balance=100, category="test", credit_status=1, reference_id="test_reference_id", associated_user=self.user.profile)

	def test_create_user_profile(self):
		"""Test the customer or user creation model can create user and profile objects."""
		self.assertEqual(self.user.username, "username1")
		self.assertEqual(self.user.profile.user_xid, uuid.UUID("ea0212d3-abd6-406f-8c67-868e814a2436").hex)

	def test_model_can_create_master_wallet(self):
		"""Test the master wallet model can create a MasterWallet."""
		old_count = MasterWallet.objects.count()
		self.master_wallet.save()
		new_count = MasterWallet.objects.count()
		self.assertNotEqual(old_count, new_count)

	def test_model_can_create_transaction(self):
		"""Test the wallet transaction model can create a WalletTransaction."""
		old_count = WalletTransaction.objects.count()
		self.wallet_transaction.save()
		new_count = WalletTransaction.objects.count()
		self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
	"""Test suite for the api views."""

	def setUp(self):
		"""Define the test client and other test variables."""
		self.client = APIClient()
		self.initialize_data = {'customer_xid': 'ea0212d3-abd6-406f-8c67-868e814a2436'}
		self.response = self.client.post(
										reverse('mini_wallet:init_wallet'),
										self.initialize_data,
										format="json"
										)
		response_json = self.response.json()
		self.api_token = response_json['data']['token']

	def test_api_can_init_wallet(self):
		"""Test the api has initialize account for wallet."""
		# print(self.response.json())
		self.assertEqual(self.response.status_code, status.HTTP_200_OK)

	def test_api_can_get_wallet_balance(self):
		"""Test the api has get wallet balance for wallet."""
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token)
		wallet_response = self.client.get(
			reverse('mini_wallet:wallet'),
			format="json"
			)

		self.assertEqual(wallet_response.status_code, status.HTTP_200_OK)

	def test_api_can_enable_wallet(self):
		"""Test the api can enable wallet."""
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token)
		self.client.patch(
			reverse('mini_wallet:wallet'),
			format="json"
			)
		wallet_response = self.client.post(
			reverse('mini_wallet:wallet'),
			format="json"
			)

		self.assertEqual(wallet_response.status_code, status.HTTP_200_OK)

	def test_api_can_disable_wallet(self):
		"""Test the api can disable wallet."""
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token)
		self.client.post(
			reverse('mini_wallet:wallet'),
			format="json"
		)
		wallet_response = self.client.patch(
			reverse('mini_wallet:wallet'),
			format="json"
			)
		# print(wallet_response.json())

		self.assertEqual(wallet_response.status_code, status.HTTP_200_OK)

	def test_api_can_credit_transaction(self):
		"""Test the api can credit transaction."""
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token)
		
		data = {'amount': 100, 'reference_id': '50535246-dcb2-4929-8cc9-004ea06f5241'}
		response = self.client.post(
			reverse('mini_wallet:wallet_transaction', kwargs={'category': 'deposits'}),
			data,
			format="json"
			)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_api_can_debit_transaction(self):
		"""Test the api can debit transaction."""
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token)
		
		data = {'amount': 100, 'reference_id': '50535246-dcb2-4929-8cc9-004ea06f5241'}
		response = self.client.post(
			reverse('mini_wallet:wallet_transaction', kwargs={'category': 'withdrawals'}),
			data,
			format="json"
			)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_api_check_validate_transaction(self):
		"""Test the api can debit transaction."""
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token)
		
		data = {'amount': 100, 'reference_id': '50535246-dcb2-4929-8cc9-004ea06f52411111111111111'}
		response = self.client.post(
			reverse('mini_wallet:wallet_transaction', kwargs={'category': 'withdrawals'}),
			data,
			format="json"
			)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		data = {'amount': '', 'reference_id': ''}
		response = self.client.post(
			reverse('mini_wallet:wallet_transaction', kwargs={'category': 'withdrawals'}),
			data,
			format="json"
			)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
