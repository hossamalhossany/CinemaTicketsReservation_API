"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from tickets import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1 without rest framework and  without models
    path('django/jsonres', views.no_rest_no_model),

    # 2 without rest framework and from  models
    path('django/no_rest_from__model', views.no_rest_from__model),

    # 3 Functions based views
    # 3.1  GET and POST
    path('rest/FBV_List', views.FBV_List),
    # 3.2 GET , PUT, DELETE
    path('rest/FBV_List/<int:pk>', views.FBV_pk),

    # 4 CBV Class Based View
    # 4.1  list and create == GET and POST
    path('rest/CBV_lsit', views.CBV_lsit.as_view()),

]
