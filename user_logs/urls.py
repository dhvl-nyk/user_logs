"""user_insights URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from user_insights import views

# from django.contrib import admin
# from django.urls import path
# from django.conf.urls.static import static
# from django.conf import settings
# from . import views


urlpatterns = [
    path('upload_call_log_csv', views.upload_call_log_csv,name= 'upload_call_log_csv'),
    path('', views.upload_call_log_csv,name= 'upload_call_log_csv'),
    path('user_call_analytics', views.user_call_analytics,name= 'user_call_analytics'),
    path('upload_app_log_csv', views.upload_app_log_csv,name= 'upload_app_log_csv'),
    path('user_app_analytics', views.user_app_analytics,name= 'user_app_analytics'),
]
