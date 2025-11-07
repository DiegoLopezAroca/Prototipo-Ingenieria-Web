from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registros/', views.registros, name='registros'),
    path('eventos/', views.eventos, name='eventos'),
    path('eventos/<int:evento_id>/asistencia/', views.asistencia, name='asistencia'),
    path('eventos/<int:evento_id>/asistencia/lista/', views.lista_asistentes, name='lista_asistentes'),
    path('cuotas/', views.cuotas, name='cuotas'),
    path('pagos/', views.pagos_view, name='pagos'),
    path('socios/', views.socios, name='socios'),
    path('socios/<int:socio_id>/', views.detalle_socio, name='detalle_socio'),
    path('merchandising/', views.merchandising, name='merchandising'),
    path('merchandising/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('contacto/', views.contacto, name='contacto'),
    path('contacto/mensajes/', views.ver_mensajes, name="ver_mensajes")
]