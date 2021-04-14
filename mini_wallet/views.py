from django.shortcuts import render
from rest_framework import generics, status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import datetime

from .serializers import RegisterSerializer, MasterWalletSerializer, WalletTransactionSerializer
from .utils import apiSuccess, apiError
from .models import MasterWallet, WalletTransaction

# Create your views here.

class InitView(generics.GenericAPIView):
	serializer_class = RegisterSerializer

	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		return_data = None
		try:
			extra_user_data = {
				'username': request.data['username'] if "username" in request.data else request.data['customer_xid'],
				'email': request.data['email'] if "email" in request.data else request.data['customer_xid']+'@test.com',
				'password': request.data['password'] if "password" in request.data else request.data['customer_xid'],
				'password2': request.data['password2'] if "password2" in request.data else request.data['customer_xid'],
				'first_name': request.data['first_name'] if "first_name" in request.data else 'User',
				'last_name': request.data['last_name'] if "last_name" in request.data else 'User',
			}

			data = serializer.validated_data
			return_data = serializer.create(data, extra_user_data) # return_data initialisation completed

		except Exception as e:
			return Response(apiError(e))

		return Response(apiSuccess(return_data), status=status.HTTP_200_OK)



class WalletAPIView(generics.GenericAPIView):
	"""
	View to manage wallet in the system.

	* Requires token authentication.
	"""
	authentication_classes = [authentication.TokenAuthentication]
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = MasterWalletSerializer

	def get(self, request, *args, **kwargs):
		"""
		Return wallet balance.
		"""
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		return_data = None

		try:
			data = serializer.validated_data
			return_data = serializer.get_balance(data, user=request.user.profile) # return_data - completed

		except Exception as e:
			return Response(apiError(e))

		return Response(apiSuccess(return_data), status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		"""
		Enable wallet.
		"""
		
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		return_data = None
		try:
			data = serializer.validated_data
			return_data = serializer.enable_wallet(data, user=request.user.profile) # return_data - completed

		except Exception as e:
			return Response(apiError(e))

		return Response(apiSuccess(return_data), status=status.HTTP_200_OK)

	def patch(self, request, *args, **kwargs):
		"""
		Disable wallet.
		"""
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		return_data = None
		try:
			data = serializer.validated_data
			return_data = serializer.disable_wallet(data, user=request.user.profile) # return_data - completed

		except Exception as e:
			return Response(apiError(e))

		return Response(apiSuccess(return_data), status=status.HTTP_200_OK)


class WalletTransactionAPIView(generics.GenericAPIView):
	"""
	View to perform transaction in the wallet.

	* Requires token authentication.
	"""
	authentication_classes = [authentication.TokenAuthentication]
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = WalletTransactionSerializer

	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		return_data = None
		category = kwargs['category'] if "category" in kwargs else None
		try:
			if category:
				data = serializer.validated_data
			
				return_data = serializer.create(data, user=request.user.profile, category=category) # return_data - completed

		except Exception as e:
			return Response(apiError(e))

		return Response(apiSuccess(return_data), status=status.HTTP_200_OK)
