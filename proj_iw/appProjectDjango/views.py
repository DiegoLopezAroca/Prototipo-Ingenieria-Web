from django.shortcuts import render, get_object_or_404, redirect
from .models import Socio, Eventos, Cuotas, Merchandising
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

# Vista principal
def index(request):
    return render(request, 'index.html')

# Vista de socios (lista)
def socios(request):
    lista_socios = Socio.objects.all()
    contexto = {'socios': lista_socios}
    return render(request, 'lista_socios.html', contexto)

# Vista de detalle de socio
@user_passes_test(lambda u: u.is_superuser)
def detalle_socio(request, socio_id):
    socio = get_object_or_404(Socio, id=socio_id)
    contexto = {'socio': socio}
    return render(request, 'detalle_socio.html', contexto)

def cuotas(request):
    cuotas = Cuotas.objects.all()
    return render(request, 'cuotas.html', {'cuotas': cuotas})

# Vista de merchandising (lista)
def merchandising(request):
    merchandising = Merchandising.objects.all()
    contexto = {'merchandisings': merchandising}
    return render(request, 'merchandising.html', contexto)

# Vista de detalle de merchandising
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Merchandising, id=producto_id)
    contexto = {'producto': producto}
    return render(request, 'lista_merchandising.html', contexto)

def registros(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        segundo_apellido = request.POST.get('segundo_apellido')
        mayor13 = request.POST.get('mayor13') == 'True'
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        telefono = request.POST.get('telefono')

        if mayor13:
            tipo_socio = request.POST.get('tipo_socio') or 'nuevo'
        else:
            tipo_socio = 'menor'

        # Validaciones
        if password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registros')

        if Socio.objects.filter(email=email).exists():
            messages.error(request, "El email ya está registrado.")
            return redirect('registros')

        # Crear socio
        Socio.objects.create(
            nombre=nombre,
            apellido=apellido,
            segundo_apellido=segundo_apellido,
            mayor13=mayor13,
            fecha_nacimiento=fecha_nacimiento or None,
            tipo_socio=tipo_socio,
            email=email,
            password=password,
            telefono=telefono
        )

        messages.success(request, "Registro completado con éxito.")
        return redirect('socios')

    return render(request, 'registro.html')