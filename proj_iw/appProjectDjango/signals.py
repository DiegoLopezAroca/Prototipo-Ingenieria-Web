from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Socio, Cuotas, Pagos
from datetime import date

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
