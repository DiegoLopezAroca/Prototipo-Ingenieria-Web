from django.shortcuts import render, get_object_or_404, redirect
from appProjectDjango.models import Socio, Eventos, Cuotas, Merchandising, Pagos, Contacto, AsistenciaEvento
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone


# Vista principal
def index(request):
    return render(request, 'index.html')

# Vista de eventos (lista)
@user_passes_test(lambda u: u.is_superuser)
def eventos(request):
    lista_eventos = Eventos.objects.all()
    contexto = {'eventos': lista_eventos}
    return render(request, 'eventos.html', contexto)

# Vista de socios (lista)
def socios(request):
    lista_socios = Socio.objects.all()
    contexto = {'socios': lista_socios}
    return render(request, 'lista_socios.html', contexto)

# Vista de asistencia a eventos
@user_passes_test(lambda u: u.is_superuser)
def asistencia(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if not email:
            messages.error(request, "Introduce tu email para apuntarte.")
        else:
            socio = Socio.objects.filter(email=email).first()
            if not socio:
                messages.error(request, "¡ATENCIÓN! Ese email no está registrado. Regístrate antes de apuntarte.")
                return redirect("registros")  # o vuelve a la misma página si prefieres
            # Evitar duplicados
            ya_apuntado = AsistenciaEvento.objects.filter(evento=evento, socio=socio).exists()
            if ya_apuntado:
                messages.info(request, "¡ATENCIÓN! Ya estabas inscrito en este evento.")
            else:
                AsistenciaEvento.objects.create(evento=evento, socio=socio)
                messages.success(request, "¡Apuntado correctamente!")
        return redirect("asistencia", evento_id=evento.id)

    asistentes = AsistenciaEvento.objects.filter(evento=evento).select_related("socio").order_by("-fecha_registro")
    return render(request, "asistencia.html", {"evento": evento, "asistentes": asistentes})

# Vista para listar los asistentes a un evento (solo admin)
@user_passes_test(lambda u: u.is_superuser)
def lista_asistentes(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)
    asistentes = AsistenciaEvento.objects.filter(evento=evento).select_related("socio").order_by("socio__nombre")
    return render(request, "lista_asistentes.html", {"evento": evento, "asistentes": asistentes})

# Vista de detalle de socio
@user_passes_test(lambda u: u.is_superuser)
def detalle_socio(request, socio_id):
    socio = get_object_or_404(Socio, id=socio_id)
    contexto = {'socio': socio}
    return render(request, 'detalle_socio.html', contexto)

def cuotas(request):
    cuotas = Cuotas.objects.all()
    return render(request, 'cuotas.html', {'cuotas': cuotas})

# Solo permitir acceso a administradores
@user_passes_test(lambda u: u.is_superuser)
def pagos_view(request):
    pagos = Pagos.objects.select_related('socio', 'cuota').all().order_by('-fecha_pago')
    socio_id = request.GET.get('socio_id')
    return render(request, 'pagos.html', {'pagos': pagos, 'socio_id': socio_id})

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

def contacto(request):
    # --- AJAX GET: comprobar email (para activar el textarea y botón) ---
    if request.method == "GET" and "email" in request.GET:
        email = request.GET.get("email", "").strip()
        existe = Socio.objects.filter(email=email).exists()
        return JsonResponse({"existe": existe})

    # --- POST: enviar mensaje ---
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        mensaje = request.POST.get("mensaje", "").strip()

        # Validaciones básicas
        if not email:
            return render(request, "contacto.html", {"error": "Introduce un correo electrónico."})
        if not mensaje:
            return render(request, "contacto.html", {"error": "Escribe un mensaje antes de enviar."})

        socio = Socio.objects.filter(email=email).first()

        if not socio:
            return render(request, "contacto.html", {
                "error": "El email no está registrado. Por favor, regístrate antes de enviar un mensaje."
            })

        # Guardar el mensaje en la tabla Contacto
        Contacto.objects.create(
            socio=socio,
            email=email,
            mensaje=mensaje,
            # fecha_envio se autogenera si en el modelo usas auto_now_add=True
        )

        return render(request, "contacto.html", {
            "exito": "Mensaje enviado correctamente. ¡Gracias por contactar con nosotros!"
        })

    # --- GET normal: mostrar formulario ---
    return render(request, "contacto.html")

# Vista para listar los mensajes de contacto (solo admin)
@user_passes_test(lambda u: u.is_superuser)
def ver_mensajes(request):
    mensajes = Contacto.objects.select_related('socio').all().order_by('-fecha_envio')
    return render(request, "ver_mensajes.html", {"mensajes": mensajes})