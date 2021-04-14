from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
	path('signup/', views.InsSignup.as_view(), name='signup'),
 	path('logout/', views.InsLogoutView.as_view(), name='ins_logout'),
	path('dashboard/', views.InsDashboard.as_view(), name='dashboard'),

	# profile
	path('profile/', views.MyProfile.as_view(), name ='profile'),
	path('profile/display-picture/', views.DpChange.as_view(), name ='dp_change'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)