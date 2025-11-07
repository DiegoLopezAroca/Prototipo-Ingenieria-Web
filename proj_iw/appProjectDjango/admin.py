from django.contrib import admin
from .models import Socio, Eventos, Cuotas, Merchandising, Pagos, Contacto, AsistenciaEvento

# Register your models here.
admin.site.register(Socio)
admin.site.register(Eventos)
admin.site.register(Cuotas)
admin.site.register(Merchandising)
admin.site.register(Pagos)
admin.site.register(Contacto)
admin.site.register(AsistenciaEvento)