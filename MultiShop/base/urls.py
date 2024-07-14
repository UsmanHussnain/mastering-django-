# myapp/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import signup, index_view, login_view , verify_email ,send_email_verification , logoutUser, dashboard , editProfile , profile_detail, change_password, home

urlpatterns = [
    path('', home , name = 'home'),
    path('index/', index_view, name='index'),  
    path('dashboard/', dashboard, name='dashboard'),

    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logoutUser/', logoutUser, name='logoutUser'),

    path('send-email/', send_email_verification, name='send_email'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
    
    path('profile-detail/', profile_detail, name='profile-detail'),
    path('edit-profile/', editProfile, name='edit-profile'),
    
    path('change-password/',change_password, name='change-password'),





] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)