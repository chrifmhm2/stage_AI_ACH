# """
# URL configuration for mydjangosite project.
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path
# from . import views
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.index, name='index'),
#     path('userreg/', views.userreg, name='userreg'),
#     path('insertuser/', views.insertuser, name='insertuser'),
#     path('viewusers/', views.viewusers, name='viewusers'),
#     path('deleteprofile/<str:id>', views.deleteprofile, name='deleteprofile'),
#     path('editprofile/<str:id>', views.editprofile, name='editprofile'),
#     path('updateprofile/<str:id>', views.updateprofile, name='updateprofile'),
# ]
#
# urlpatterns += staticfiles_urlpatterns()

from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('', views.index, name='index'),
    path('generateTemplate/', views.generateTemplate, name='generateTemplate'),
    path('ajax/load-accounts/', views.ajax_load_accounts, name='ajax_load_accounts'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
]
# urlpatterns += staticfiles_urlpatterns()
# path('ajax/load-accounts/', views.ajax_load_accounts, name='ajax_load_accounts'),

# path('generateTemplate/', views.generateTemplate, name='generateTemplate'),
