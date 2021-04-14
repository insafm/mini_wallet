from django.test import TestCase

from django.contrib.auth.models import User
from ins_user.util import custom_send_mail

# Create your tests here.

class ApiTestCaseSendMail(TestCase):
	def setUp(self):
		pass

	def test_send_mail(self):
		user = User.objects.create(first_name="first_name", last_name="last_name", email="insishere@mailinator.net", username="username1", password='Abc@12345')

		user.refresh_from_db()
		user.profile.user_type = "education"
		user.save()

		params = {}
		params['recipient_list'] = [user.email]
		params['subject'] = "Welcome to Site"
		params['message'] = f'Hi {user.username}, thank you for registering in our site.'
		
		self.assertTrue(custom_send_mail(params))
