"""esp1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from user import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("modmain.urls")),
    path('register/', user_views.register, name='register-url'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/Tournaments',user_views.profile_tournaments,name="user_tournaments"),
    path('profile/Tournaments/wins',user_views.profile_wins,name="user_wins"),
    path('addFavroutes/', user_views.favroutes, name='Favroutes'),
    path('success/', user_views.addmoney, name='addmoneysuccess'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('addprofiledetails/', user_views.updateprofile, name='addprofiledetails'),
    path('profile/editprofiledetails/', user_views.editprofile, name='editprofiledetails'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('profile/wallet',user_views.profile_wallet,name="wallet"),
    path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('profile/Teams',user_views.totalteams,name="Teams"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)