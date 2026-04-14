"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from myapp import views        

urlpatterns = [
    path("", views.un_home),
    path("server/", views.server_chat),
    path("log_out/", views.log_out),
    path("admin/", admin.site.urls),
    path("home/", views.home),
    path("log_in/", views.login_user),
    path("register/", views.register_page),
    path("banned/", views.your_banned_lol),
    path("edit_profile_page/", views.edit_profile_page),
    path("change_username/", views.change_username),
    path("change_password/", views.change_password),
    path("change_picture/", views.change_picture),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

