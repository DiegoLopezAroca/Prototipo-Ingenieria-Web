from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Socio, Eventos, Cuotas, Merchandising, Pagos, Contacto, AsistenciaEvento, SocioForm

# -------------------------
# VISTA PRINCIPAL
# -------------------------
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

# -------------------------
# LISTADOS
# -------------------------
class EventosListView(ListView):
    model = Eventos
    template_name = 'eventos.html'
    context_object_name = 'eventos'

class SociosListView(ListView):
    model = Socio
    template_name = 'lista_socios.html'
    context_object_name = 'socios'

class CuotasListView(ListView):
    model = Cuotas
    template_name = 'cuotas.html'
    context_object_name = 'cuotas'

class MerchandisingListView(ListView):
    model = Merchandising
    template_name = 'merchandising.html'
    context_object_name = 'merchandisings'

# -------------------------
# DETALLES
# -------------------------
class SocioDetailView(UserPassesTestMixin, DetailView):
    model = Socio
    template_name = 'detalle_socio.html'
    pk_url_kwarg = 'socio_id'
    context_object_name = 'socio'

    def test_func(self):
        return self.request.user.is_superuser

class ProductoDetailView(DetailView):
    model = Merchandising
    template_name = 'lista_merchandising.html'
    pk_url_kwarg = 'producto_id'
    context_object_name = 'producto'

# -------------------------
# REGISTRO DE SOCIOS
# -------------------------
class RegistroView(CreateView):
    model = Socio
    form_class = SocioForm
    template_name = 'registro.html'
    success_url = reverse_lazy('socios')

# -------------------------
# CONTACTO
# -------------------------
class ContactoView(View):
    def get(self, request):
        email = request.GET.get("email", "").strip()
        if email:
            existe = Socio.objects.filter(email=email).exists()
            return JsonResponse({"existe": existe})
        return render(request, "contacto.html")

    def post(self, request):
        email = request.POST.get("email", "").strip()
        mensaje = request.POST.get("mensaje", "").strip()

        if not email:
            return render(request, "contacto.html", {"error": "Introduce un correo electrónico."})
        if not mensaje:
            return render(request, "contacto.html", {"error": "Escribe un mensaje antes de enviar."})

        socio = Socio.objects.filter(email=email).first()
        if not socio:
            return render(request, "contacto.html", {
                "error": "El email no está registrado. Por favor, regístrate antes de enviar un mensaje."
            })

        Contacto.objects.create(socio=socio, email=email, mensaje=mensaje)
        return render(request, "contacto.html", {"exito": "Mensaje enviado correctamente. ¡Gracias por contactar con nosotros!"})

# -------------------------
# ASISTENCIA A EVENTOS
# -------------------------
class AsistenciaView(View):
    def get(self, request, evento_id):
        evento = get_object_or_404(Eventos, id=evento_id)
        asistentes = AsistenciaEvento.objects.filter(evento=evento).select_related("socio").order_by("-fecha_registro")
        return render(request, "asistencia.html", {"evento": evento, "asistentes": asistentes})

    def post(self, request, evento_id):
        evento = get_object_or_404(Eventos, id=evento_id)
        email = request.POST.get("email", "").strip()

        if not email:
            messages.error(request, "Introduce tu email para apuntarte.")
        else:
            socio = Socio.objects.filter(email=email).first()
            if not socio:
                messages.error(request, "¡ATENCIÓN! Ese email no está registrado. Regístrate antes de apuntarte.")
                return redirect("registros")
            if AsistenciaEvento.objects.filter(evento=evento, socio=socio).exists():
                messages.info(request, "¡ATENCIÓN! Ya estabas inscrito en este evento.")
            else:
                AsistenciaEvento.objects.create(evento=evento, socio=socio)
                messages.success(request, "¡Apuntado correctamente!")
        return redirect("asistencia", evento_id=evento.id)

# -------------------------
# LISTA DE ASISTENTES (ADMIN)
# -------------------------
class ListaAsistentesView(UserPassesTestMixin, ListView):
    model = AsistenciaEvento
    template_name = "lista_asistentes.html"
    context_object_name = "asistentes"

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        evento_id = self.kwargs['evento_id']
        return AsistenciaEvento.objects.filter(evento_id=evento_id).select_related('socio').order_by('socio__nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evento'] = get_object_or_404(Eventos, id=self.kwargs['evento_id'])
        return context

# -------------------------
# PAGOS (ADMIN)
# -------------------------
class PagosView(UserPassesTestMixin, ListView):
    model = Pagos
    template_name = 'pagos.html'
    context_object_name = 'pagos'

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return Pagos.objects.select_related('socio', 'cuota').all().order_by('-fecha_pago')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['socio_id'] = self.request.GET.get('socio_id')
        return context

# -------------------------
# VER MENSAJES DE CONTACTO (ADMIN)
# -------------------------
class VerMensajesView(UserPassesTestMixin, ListView):
    model = Contacto
    template_name = "ver_mensajes.html"
    context_object_name = "mensajes"

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return Contacto.objects.select_related('socio').all().order_by('-fecha_envio')
