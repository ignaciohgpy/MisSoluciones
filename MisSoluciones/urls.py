"""MisSoluciones URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from Soluciones.views import *
from django.conf import settings
from django.conf.urls.static import static






urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index,name='index'),
    path('problema/<str:libro>', problema,name='problema'),
    path('cargar', cargar, name="cargar"),
    path('versolucion/<str:libro>/<str:numero>', versolucion,name='versolucion'),
    path('login/', Login.as_view(template_name='login.html'), name="login"),
    path('logout/', Logout.as_view(template_name='logout.html'), name="logout"),
    path('registrarse/', registrarse, name="registrarse"),
    path('ajax/compraPKT/', compraPKT, name='compraPKT'),
    path('ajax/verPKT/', verPKT, name='verPKT'),
    path('ajax/getProblemas/', getProblemas, name='getProblemas'),
    path('ListaLibros/', Addlibros.as_view(),name="ListaL"),
    path('ver/', ver,name="ver"),
    path('ejemplo/', ejemplo,name="ejemplo"),
    path('busquedas/', consultar,name="consultar"),
    path('verMiPKT/<str:pkt>', mipkt,name="mipkt"),
    path('ajax/borraPa/', borraPa, name='borraPa'),
    path('ajax/getPaquetes/', getPaquetes, name='getPaquetes'),
    path('ajax/getDetalles/', getDetalles, name='getDetalles'),
    path('ajax/TranferMovil/', TranferMovil, name='TranferMovil'),
    path('TranferMovil/<str:pkt>/<str:usuario>', TranferMovil, name='TranferMovil'),
    path('acerca/', acerca,name="acerca"),
    ]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

