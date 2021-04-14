from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField

import pprint
pp = pprint.pprint

class ProfileForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, help_text='Required.')
	last_name = forms.CharField(max_length=30, help_text='Required.')
	email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

	birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'birth_date')


from ins_user.models import Profile
class DpChangeForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ('dp',)
	
	def __init__(self, *args, **kwargs):
		super(DpChangeForm,self).__init__(*args, **kwargs)

	def save(self, commit=True, **kwargs):
		photo = super(DpChangeForm, self).save()
		
		# profile = None
		# if "profile" in self.initial:
		# 	profile = self.initial['profile']
		# if self.cleaned_data['image_caption'] and profile:
		# 	profile.image_caption = self.cleaned_data['image_caption']
		# 	profile.uploaded_status = 1
		# 	profile.status = True
		# 	profile.save()
		return photo


class InsSignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, help_text='Required.')
	last_name = forms.CharField(max_length=30, help_text='Required.')
	email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
	# birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

	CHOICES =( 
		("education", "Education"), 
		("recreational", "Recreational"), 
		("social", "Social"), 
		("diy", "Diy"), 
		("charity", "Charity"), 
		("cooking", "Cooking"), 
		("relaxation", "Relaxation"), 
		("music", "Music"), 
		("busywork", "Busywork"), 
	) 
	user_type = forms.ChoiceField(choices=CHOICES, help_text='Required.')
	captcha = ReCaptchaField()

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
