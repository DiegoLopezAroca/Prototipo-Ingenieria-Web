from django.db import models

# Create your models here.
class Socio(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return f"id={self.id}, nombre={self.nombre}, telefono={self.telefono},email={self.email}"
    
class Eventos(models.Model):
    nombre = models.CharField(max_length=50)
    fecha = models.DateField()
    descripcion = models.TextField()
    lugar = models.CharField(max_length=100)

    def __str__(self):
        return f"id={self.id}, nombre={self.nombre}, fecha={self.fecha}, lugar={self.lugar}, descripcion={self.descripcion}"
    
class Cuotas(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return f"id={self.id}, socio={self.socio.nombre}, monto={self.monto}, fecha_pago={self.fecha_pago}, descripcion={self.descripcion}"
    
class Merchandising(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.CharField(max_length=100, default='default.png')

    def __str__(self):
        return f"id={self.id}, nombre={self.nombre}, precio={self.precio}, descripcion={self.descripcion}, imagen={self.imagen}"