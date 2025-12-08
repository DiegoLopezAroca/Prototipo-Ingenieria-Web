from django.db import models
from django import forms
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import check_password

# -------------------------
# MODELOS
# -------------------------
class Socio(models.Model):
    # TIPO_SOCIO_CHOICES = [
    #     ('menor', 'Menor'),
    #     ('socio', 'Socio'),
    #     ('nuevo', 'Nuevo'),
    # ]

    nombre = models.CharField(max_length=100, db_index=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    mayor13 = models.BooleanField(default=True)
    fecha_nacimiento = models.DateField(blank=True, null=True, db_index=True)
    tipo_socio = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    telefono = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\d+$', 'El teléfono solo puede contener números')]
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo_socio})"
    
    class Meta:
        db_table = "Socios"


class Eventos(models.Model):
    nombre = models.CharField(max_length=50, db_index=True)
    fecha = models.DateField(db_index=True)
    descripcion = models.TextField()
    lugar = models.CharField(max_length=100)
    imagen = models.CharField(max_length=100, default='default.png')

    def __str__(self):
        return f"id={self.id}, nombre={self.nombre}, fecha={self.fecha}, lugar={self.lugar}, descripcion={self.descripcion}, imagen={self.imagen}"

    class Meta:
        db_table = "Eventos"


class Cuotas(models.Model):
    tipo_socio = models.CharField(max_length=50, null=True, blank=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)
    beneficios = models.TextField()

    def __str__(self):
        return f"{self.tipo_socio} - {self.precio}€"
    
    class Meta:
        db_table = "Cuotas"


class Pagos(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="pagos")
    cuota = models.ForeignKey(Cuotas, on_delete=models.CASCADE, related_name="pagos")
    fecha_pago = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Pago de {self.socio.nombre} - {self.cuota.tipo_socio} ({self.fecha_pago})"
    
    class Meta:
        db_table = "Pagos"


class Merchandising(models.Model):
    nombre = models.CharField(max_length=50, db_index=True)
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
    email = models.EmailField(db_index=True)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Mensaje de {self.email} - {self.fecha_envio.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        db_table = "Contactos"


class AsistenciaEvento(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="asistencias")
    evento = models.ForeignKey(Eventos, on_delete=models.CASCADE, related_name="asistencias")
    fecha_registro = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Asistencia de {self.socio.nombre} al evento {self.evento.nombre}"
    
    class Meta:
        unique_together = ("socio", "evento")
        db_table = "AsistenciaEvento"


# -------------------------
# FORMULARIOS BASADOS EN MODELOS
# -------------------------
class SocioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = Socio
        fields = [
            'nombre', 'apellido', 'segundo_apellido',
            'mayor13', 'fecha_nacimiento', 'tipo_socio',
            'email', 'password', 'telefono'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # BooleanField -> radios Sí/No
        self.fields['mayor13'].widget = forms.RadioSelect(
            choices=[
                (True, 'Sí'),
                (False, 'No'),
            ]
        )
        cuotas = Cuotas.objects.all()
        self.fields['tipo_socio'] = forms.ChoiceField(
            choices=[("", "-- Selecciona una cuota --")] + [
                (c.tipo_socio, f"{c.tipo_socio} - {c.precio}€") for c in cuotas
            ],
            required=False,
            label="Tipo de cuota",
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or "@" not in email:
            raise forms.ValidationError("Introduce un correo electrónico válido.")
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo puede contener números.")
        return telefono

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            self.add_error('password_confirm', "Las contraseñas no coinciden")
        else:
            cleaned_data['password'] = make_password(cleaned_data['password'])
        return cleaned_data

class SocioEditarForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = [
            'nombre', 'apellido', 'segundo_apellido', 'mayor13',
            'fecha_nacimiento', 'tipo_socio', 'email', 'telefono'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or "@" not in email:
            raise forms.ValidationError("Introduce un correo electrónico válido.")
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo puede contener números.")
        return telefono


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['email', 'mensaje']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or "@" not in email:
            raise forms.ValidationError("Introduce un correo electrónico válido.")
        return email

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje')
        if not mensaje or len(mensaje.strip()) < 5:
            raise forms.ValidationError("El mensaje debe tener al menos 5 caracteres.")
        return mensaje


class AsistenciaEventoForm(forms.ModelForm):
    email = forms.EmailField(label="Email con el que te registraste")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = AsistenciaEvento
        fields = []  # no pedimos socio directamente

    def clean_email(self):
        email = self.cleaned_data.get('email')
        socio = Socio.objects.filter(email=email).first()
        if not socio:
            raise forms.ValidationError("No se encontró ningún socio con ese email.")
        # guardamos el socio encontrado para usarlo en la vista
        self.cleaned_data['socio'] = socio
        return email
    
    def clean(self):
        cleaned = super().clean()
        socio = cleaned.get('socio')
        password = cleaned.get('password')

        if socio and password:
            guardada = socio.password or ""
            ok = False

            if guardada.startswith("pbkdf2_"):
                # Caso: ya está hasheada
                ok = check_password(password, guardada)
            else:
                # Caso antiguo: texto plano
                if guardada == password:
                    ok = True
                    # Aprovechamos para actualizarla a hash
                    socio.password = make_password(password)
                    socio.save(update_fields=["password"])

            if not ok:
                self.add_error('password', "Contraseña incorrecta.")

        return cleaned

class AsistenciaEventoAdminForm(forms.ModelForm):
    email = forms.EmailField(label="Email del socio")

    class Meta:
        model = AsistenciaEvento
        fields = []  # no pedimos socio directamente

    def clean_email(self):
        email = self.cleaned_data.get('email')
        socio = Socio.objects.filter(email=email).first()
        if not socio:
            raise forms.ValidationError("No se encontró ningún socio con ese email.")
        self.cleaned_data['socio'] = socio
        return email


class CuotaForm(forms.ModelForm):
    class Meta:
        model = Cuotas
        fields = ['tipo_socio', 'precio', 'beneficios']
        widgets = {
            'beneficios': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is None or precio <= 0:
            raise forms.ValidationError("El precio debe ser un número positivo.")
        return precio

class MerchandisingForm(forms.ModelForm):
    class Meta:
        model = Merchandising
        fields = ['nombre', 'precio', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        instancia = super().save(commit=False)
        # asignar imagen por defecto
        instancia.imagen = 'no_pic.png'
        instancia.imagen2 = 'no_pic.png'
        if commit:
            instancia.save()
        return instancia

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is None or precio <= 0:
            raise forms.ValidationError("El precio debe ser un número positivo.")
        return precio

class EventoForm(forms.ModelForm):
    class Meta:
        model = Eventos
        fields = ['nombre', 'fecha', 'descripcion', 'lugar']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }
