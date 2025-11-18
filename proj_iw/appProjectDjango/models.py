from django.db import models
from django import forms

# Create your models here.
class Socio(models.Model):
    TIPO_SOCIO_CHOICES = [
        ('menor', 'Menor'),
        ('socio', 'Socio'),
        ('nuevo', 'Nuevo'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    mayor13 = models.BooleanField(default=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    tipo_socio = models.CharField(max_length=20, choices=TIPO_SOCIO_CHOICES, default='nuevo')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo_socio})"
    
    class Meta:
        db_table = "Socios"
    
class Eventos(models.Model):
    nombre = models.CharField(max_length=50)
    fecha = models.DateField()
    descripcion = models.TextField()
    lugar = models.CharField(max_length=100)
    imagen = models.CharField(max_length=100, default='default.png')

    def __str__(self):
        return f"id={self.id}, nombre={self.nombre}, fecha={self.fecha}, lugar={self.lugar}, descripcion={self.descripcion}, imagen={self.imagen}"

    class Meta:
        db_table = "Eventos"

class Cuotas(models.Model):
    tipo_socio = models.CharField(max_length=50, null=True, blank=True)  # "Adulto", "Niño", "Socio nuevo"
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)
    beneficios = models.TextField()

    def __str__(self):
        return f"{self.tipo_socio} - {self.precio}€"
    
    class Meta:
        db_table = "Cuotas"

class Pagos(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="pagos")
    cuota = models.ForeignKey(Cuotas, on_delete=models.CASCADE, related_name="pagos")
    fecha_pago = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pago de {self.socio.nombre} - {self.cuota.tipo_socio} ({self.fecha_pago})"
    
    class Meta:
        db_table = "Pagos"

class Merchandising(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.CharField(max_length=100, default='default.png')
    imagen2 = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"id={self.id}, nombre={self.nombre}, precio={self.precio}, descripcion={self.descripcion}, imagen={self.imagen},imagen2={self.imagen2}"

    class Meta:
        db_table = "Merchandising"


class Contacto(models.Model):
    socio = models.ForeignKey('Socio', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.email} - {self.fecha_envio.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        db_table = "Contactos"

class AsistenciaEvento(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="asistencias")
    evento = models.ForeignKey(Eventos, on_delete=models.CASCADE, related_name="asistencias")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asistencia de {self.socio.nombre} al evento {self.evento.nombre}"
    
    class Meta:
        unique_together = ("socio", "evento") # evitar duplicados
        db_table = "AsistenciaEvento"

class SocioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = Socio
        fields = ['nombre', 'apellido', 'segundo_apellido', 'mayor13', 'fecha_nacimiento', 'tipo_socio', 'email', 'password', 'telefono']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            self.add_error('password_confirm', "Las contraseñas no coinciden")
        return cleaned_data

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['email', 'mensaje']