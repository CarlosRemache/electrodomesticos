#URLS especificas de la aplicacion
from django.urls import path

from.import views
urlpatterns = [

   # LOGIN
    path('', views.login_view, name='login'),
    path('menu/', views.menu_view, name='menu'),
    path('cerrar/', views.cerrar_sesion, name='cerrar_sesion'),

    path('',views.inicio),
    path('inicio/', views.inicio, name='inicio'),
    path('contacto/', views.contacto),
    path('servicio/', views.servicio),

    
    path('nuevologin/', views.nuevologin),
    path('listadologin/', views.listadologin),
    path('guardarlogin/', views.guardarlogin),
    path('eliminarlogin/<int:id>/', views.eliminarlogin),
    path('editarlogin/<int:id>/', views.editarlogin),
    path('procesareditarlogin/', views.procesareditarlogin),


    path('nuevocliente/', views.nuevocliente),
    path('listadocliente/', views.listadocliente),
    path('guardarcliente/', views.guardarcliente),
    path('eliminarcliente/<int:id>/', views.eliminarcliente),
    path('editarcliente/<int:id>/', views.editarcliente),
    path('procesareditarcliente/', views.procesareditarcliente),



    path('nuevotecnico/', views.nuevotecnico),
    path('listadotecnico/', views.listadotecnico),
    path('guardartecnico/', views.guardartecnico),
    path('eliminartecnico/<int:id>/', views.eliminartecnico),
    path('editartecnico/<int:id>/', views.editartecnico),
    path('procesareditartecnico/', views.procesareditartecnico),


    path('nuevoelectrodomestico/', views.nuevoelectrodomestico),
    path('listadoelectrodomestico/', views.listadoelectrodomestico),
    path('guardarelectrodomestico/', views.guardarelectrodomestico),
    path('eliminarelectrodomestico/<int:id>/', views.eliminarelectrodomestico),
    path('editarelectrodomestico/<int:id>/', views.editarelectrodomestico),
    path('procesareditarelectrodomestico/', views.procesareditarelectrodomestico),


    path('nuevoservicio/', views.nuevoservicio),
    path('listadoservicio/', views.listadoservicio),
    path('guardarservicio/', views.guardarservicio),
    path('eliminarservicio/<int:id>/', views.eliminarservicio),
    path('editarservicio/<int:id>/', views.editarservicio),
    path('procesareditarservicio/', views.procesareditarservicio),

    path('nuevafactura/', views.nuevafactura),
    path('listadofactura/', views.listadofactura),
    path('guardarfactura/', views.guardarfactura),
    path('eliminarfactura/<int:id>/', views.eliminarfactura),
    path('editarfactura/<int:id>/', views.editarfactura),
    path('procesareditarfactura/', views.procesareditarfactura),

]


