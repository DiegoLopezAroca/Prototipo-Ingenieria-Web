from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registros/', views.registros, name='registros'),
    #path('eventos/', views.eventos, name='eventos'),
    #path('eventos/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    #path('eventos/<int:evento_id>/socios/', views.socios_evento, name='socios_evento'),
    path('cuotas/', views.cuotas, name='cuotas'),
    #path('cuotas/<int:cuota_id>/', views.detalle_cuota, name='detalle_cuota'),
    path('socios/', views.socios, name='socios'),
    path('socios/<int:socio_id>/', views.detalle_socio, name='detalle_socio'),
    #path('merchandising/', views.merchandising, name='merchandising'),
    #path('merchandising/<int:producto_id>/', views.detalle_producto, name='detalle_producto')
]