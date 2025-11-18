from django.urls import path
from .views import (
    IndexView, RegistroView, EventosListView, AsistenciaView, ListaAsistentesView,
    CuotasListView, PagosView, SociosListView, SocioDetailView, MerchandisingListView,
    ProductoDetailView, ContactoView, VerMensajesView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registros/', RegistroView.as_view(), name='registros'),
    path('eventos/', EventosListView.as_view(), name='eventos'),
    path('eventos/<int:evento_id>/asistencia/', AsistenciaView.as_view(), name='asistencia'),
    path('eventos/<int:evento_id>/asistencia/lista/', ListaAsistentesView.as_view(), name='lista_asistentes'),
    path('cuotas/', CuotasListView.as_view(), name='cuotas'),
    path('pagos/', PagosView.as_view(), name='pagos'),
    path('socios/', SociosListView.as_view(), name='socios'),
    path('socios/<int:socio_id>/', SocioDetailView.as_view(), name='detalle_socio'),
    path('merchandising/', MerchandisingListView.as_view(), name='merchandising'),
    path('merchandising/<int:producto_id>/', ProductoDetailView.as_view(), name='detalle_producto'),
    path('contacto/', ContactoView.as_view(), name='contacto'),
    path('contacto/mensajes/', VerMensajesView.as_view(), name='ver_mensajes'),
]
