"""
URL configuration for simple_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.urls import path, include # include brings in urls from different django apps, which makes managing many apps in a big project easier

urlpatterns = [
    path('', include('homepage.urls')),
    path('', include('members.urls')), # makes it so all urls from our members app can be reached if we prefix them with "" (in this case nothing, since it is our root)
    path('admin/', admin.site.urls),
]
