from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import Socio, Cuotas, Pagos
from datetime import date
from django.contrib.auth.models import Group, Permission
from .models import Contacto, Eventos, AsistenciaEvento, Merchandising

@receiver(post_save, sender=Socio)
def crear_pago_automatico(sender, instance, created, **kwargs):
    if created:
        # Seleccionamos la cuota correspondiente al tipo de socio
        if instance.tipo_socio == 'menor':
            cuota = Cuotas.objects.get(tipo_socio='Niños')
        elif instance.tipo_socio == 'socio':
            cuota = Cuotas.objects.get(tipo_socio='Adultos')
        else:
            cuota = Cuotas.objects.get(tipo_socio='Socios nuevos')

        # Creamos el pago automáticamente
        Pagos.objects.create(
            socio=instance,
            cuota=cuota,
            fecha_pago=date.today()
        )

# ---------------------------------------------------------
# CONFIGURACIÓN DE ROLES PERSONALIZADOS
# ---------------------------------------------------------

# Crear roles y asignar permisos
@receiver(post_migrate)
def crear_roles(sender, **kwargs):
    # Moderador
    moderador_group, created = Group.objects.get_or_create(name="Moderador")
    modelos = [Socio, Pagos, Contacto, Eventos, AsistenciaEvento, Cuotas, Merchandising]
    for modelo in modelos:
        permisos = Permission.objects.filter(
            content_type__app_label="appProjectDjango",  
            content_type__model=modelo.__name__.lower()
        )
        for p in permisos:
            if p.codename.startswith("view_"):
                moderador_group.permissions.add(p)

    # Gestor
    gestor_group, created = Group.objects.get_or_create(name="Gestor")
    for modelo in modelos:
        permisos = Permission.objects.filter(
            content_type__app_label="appProjectDjango",  
            content_type__model=modelo.__name__.lower()
        )
        for p in permisos:
            if p.codename.startswith(("view_", "add_", "change_")):
                gestor_group.permissions.add(p)