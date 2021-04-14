from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from datetime import timezone
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView

from django.contrib.auth.models import Group, Permission

import pprint
pp = pprint.pprint

from .models import Profile
from .forms import ProfileForm, DpChangeForm, InsSignUpForm
from .signals import post_create_user_signal

# Front page with login
class InsHomePage(LoginView):
	template_name = 'home.html'
	redirect_authenticated_user = True

# Logout
class InsLogoutView(LogoutView, InsHomePage):
	template_name = 'home.html'
	next_page = 'index'

# =======================================================================
# User profile abstract view
# -----------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ins_user.member_permissions', raise_exception=True), name='dispatch')
class UserProfile(View):
	template_name = 'profile.html'
	page_title = None
	model	= Profile
	context = {}
	queryfilters = {}
	order_by_field = None
	first_only = False

	def get_queryset(self):
		queryset = self.model.objects
		if self.queryfilters:
			queryset = queryset.filter(**self.queryfilters)
		if self.order_by_field:
			queryset = queryset.order_by(self.order_by_field)			
		return queryset
	def get(self, request, *args, **kwargs):
		data = self.get_queryset().values()
		if self.first_only:
			data = data.first()

		self.context['data']= data
		self.context['page_title']= self.page_title
		return render(request, self.template_name, self.context)

# User profile abstract view END
# =======================================================================

# My profile
class MyProfile(UserProfile):
	template_name = 'profile.html'
	first_only = True
	queryfilters = {}
	queryfilters['status'] = 1
	page_title = _("My Profile")

	def get_queryset(self):
		queryset = super(MyProfile, self).get_queryset()
		queryset = queryset.filter(user=self.request.user)
		return queryset


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ins_user.member_permissions', raise_exception=True), name='dispatch')
class DpChange(View):
	template_name = 'upload.html'
	form_class = DpChangeForm
	context = {}

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		self.context['form']= form
		return render(request, self.template_name, self.context)

	def post(self, request, *args, **kwargs):
		profile = Profile.objects.filter(user=request.user).first()
		initial = {}
		initial['profile'] = profile

		form = self.form_class(request.POST, request.FILES, initial=initial)
		if form.is_valid():
			image_obj = form.save()
			image_obj.dp_uploaded_at = timezone.now()
			image_obj.save()

			message = _("Enter caption...")
			messages.add_message(request, messages.INFO, message)
			return redirect('upload_caption')
		
		self.context['form']= form
		return render(request, self.template_name, self.context)


# Registration page
class InsSignup(TemplateView):
	template_name = 'signup.html'
	form_class = InsSignUpForm
	initial = {}
	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form': form})
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			cleaned_data = form.cleaned_data
			pp(cleaned_data)
			user = form.save()
			user.refresh_from_db()  # load the profile instance created by the signal
			# user.profile.birth_date = cleaned_data.get('birth_date')
			user.profile.user_type = cleaned_data.get('user_type')
			user.save()
			# add as member
			member_group, member_group_created = Group.objects.get_or_create(name='Member')
			if member_group_created:
				member_permission = Permission.objects.get(codename='member_permissions')
				member_group.permissions.add(member_permission)
			
			member_group.user_set.add(user)

			messages.add_message(request, messages.SUCCESS, "User registered successfully.")


			# Signal for doing something after user creation START
			post_create_user_signal.send(sender="InsSignup", user=user, request=request)
			
			# Signal for doing something after user creation END
			return redirect('index')
		return render(request, self.template_name, {'form': form})


# Dashboard
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ins_user.member_permissions', raise_exception=True), name='dispatch')
class InsDashboard(View):
	template_name = 'dashboard.html'
	context = {}
	def get(self, request, *args, **kwargs):
		pp(request.user)

		# photos = UserPhotoUploads.objects.all()
		# self.context['photos']= photos
		return render(request, self.template_name, self.context)