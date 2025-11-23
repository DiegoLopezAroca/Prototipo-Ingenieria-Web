from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Socio, Eventos, Cuotas, Merchandising, Pagos, Contacto, AsistenciaEvento

# ---------------------------------------------------------
# PERSONALIZACIÓN DEL PANEL ADMIN
# ---------------------------------------------------------
admin.site.site_header = "Administración Peña El Revoque"
admin.site.site_title = "Panel de gestión"
admin.site.index_title = "Panel de administración de la Peña"

# ---------------------------------------------------------
# CONFIGURACIÓN DE ROLES PERSONALIZADOS
# ---------------------------------------------------------

def crear_roles():
    """Se ejecuta al cargar admin: crea los roles si no existen"""

    # Moderador: Puede ver mensajes, pagos, socios, eventos (solo lectura)
    if not Group.objects.filter(name="Moderador").exists():
        moderador = Group.objects.create(name="Moderador")

        modelos_lectura = [Socio, Pagos, Contacto, Eventos, AsistenciaEvento, Cuotas, Merchandising]

        for modelo in modelos_lectura:
            permisos = Permission.objects.filter(
                content_type__app_label="appProjectDjango",  
                content_type__model=modelo.__name__.lower()
            )
            for p in permisos:
                if p.codename.startswith("view_"):  # solo lectura
                    moderador.permissions.add(p)

    # Gestor: puede añadir y editar, pero NO borrar
    if not Group.objects.filter(name="Gestor").exists():
        gestor = Group.objects.create(name="Gestor")

        modelos = [Socio, Pagos, Contacto, Eventos, Cuotas, Merchandising, AsistenciaEvento]

        for modelo in modelos:
            permisos = Permission.objects.filter(
                content_type__app_label="appProjectDjango", 
                content_type__model=modelo.__name__.lower()
            )
            for p in permisos:
                if p.codename.startswith(("view_", "add_", "change_")):
                    gestor.permissions.add(p)

try:
    crear_roles()
except:
    pass  # Evitar errores durante migraciones


# ---------------------------------------------------------
# ADMIN PERSONALIZADO PARA CADA MODELO
# ---------------------------------------------------------

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "email", "tipo_socio", "mayor13", "telefono")
    list_filter = ("tipo_socio", "mayor13")
    search_fields = ("nombre", "apellido", "email")
    ordering = ("apellido", "nombre")
    readonly_fields = ("password",)


@admin.register(Eventos)
class EventosAdmin(admin.ModelAdmin):
    list_display = ("nombre", "fecha", "lugar")
    search_fields = ("nombre", "lugar")
    list_filter = ("fecha",)


@admin.register(Cuotas)
class CuotasAdmin(admin.ModelAdmin):
    list_display = ("tipo_socio", "precio")
    search_fields = ("tipo_socio",)


@admin.register(Pagos)
class PagosAdmin(admin.ModelAdmin):
    list_display = ("socio", "cuota", "fecha_pago")
    list_filter = ("fecha_pago", "cuota__tipo_socio")
    search_fields = ("socio__nombre", "socio__apellido")
    autocomplete_fields = ("socio", "cuota")


@admin.register(Merchandising)
class MerchandisingAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio")
    search_fields = ("nombre",)


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("email", "socio", "fecha_envio")
    search_fields = ("email", "socio__nombre")
    list_filter = ("fecha_envio",)
    readonly_fields = ("fecha_envio",)


@admin.register(AsistenciaEvento)
class AsistenciaEventoAdmin(admin.ModelAdmin):
    list_display = ("socio", "evento", "fecha_registro")
    list_filter = ("evento",)
    autocomplete_fields = ("socio", "evento")
