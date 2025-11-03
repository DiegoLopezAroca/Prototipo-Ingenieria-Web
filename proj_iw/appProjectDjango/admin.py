from django.contrib import admin
from .models import Socio, Eventos, Cuotas, Merchandising

# Register your models here.
admin.site.register(Socio)
admin.site.register(Eventos)
admin.site.register(Cuotas)
admin.site.register(Merchandising)