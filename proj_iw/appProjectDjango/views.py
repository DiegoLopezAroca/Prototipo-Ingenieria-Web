from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import (
    Socio, Eventos, Cuotas, Merchandising, Pagos,
    Contacto, AsistenciaEvento,
    SocioForm, ContactoForm, AsistenciaEventoForm
)

# -------------------------
# FUNCIONES DE CONTROL DE ACCESO
# -------------------------
def is_moderador_o_gestor(user):
    return (
        user.is_authenticated and 
        (user.groups.filter(name="Moderador").exists() or 
         user.groups.filter(name="Gestor").exists() or 
         user.is_superuser)
    )

# -------------------------
# VISTA PRINCIPAL
# -------------------------
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

# -------------------------
# LISTADOS (con paginación y cache)
# -------------------------
@method_decorator(cache_page(60*10), name='dispatch')
class EventosListView(ListView):
    model = Eventos
    template_name = 'eventos.html'
    context_object_name = 'eventos'
    paginate_by = 20

class SociosListView(UserPassesTestMixin, ListView):
    model = Socio
    template_name = 'lista_socios.html'
    context_object_name = 'socios'
    paginate_by = 20

    def test_func(self):
        return is_moderador_o_gestor(self.request.user)

    def get_queryset(self):
        # Prefetch relaciones para evitar N+1 queries
        return Socio.objects.prefetch_related('pagos', 'asistencias').all()

class CuotasListView(ListView):
    model = Cuotas
    template_name = 'cuotas.html'
    context_object_name = 'cuotas'

class MerchandisingListView(ListView):
    model = Merchandising
    template_name = 'merchandising.html'
    context_object_name = 'merchandisings'
    paginate_by = 20

# -------------------------
# DETALLES
# -------------------------
class SocioDetailView(UserPassesTestMixin, DetailView):
    model = Socio
    template_name = 'detalle_socio.html'
    pk_url_kwarg = 'socio_id'
    context_object_name = 'socio'

    def test_func(self):
        return is_moderador_o_gestor(self.request.user)

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
        form = ContactoForm()
        return render(request, "contacto.html", {"form": form})

    def post(self, request):
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto = form.save(commit=False)
            socio = Socio.objects.filter(email=form.cleaned_data['email']).first()
            contacto.socio = socio
            contacto.save()
            messages.success(request, "Mensaje enviado correctamente. ¡Gracias por contactar con nosotros!")
            return redirect("contacto")
        messages.error(request, "Por favor corrige los errores del formulario.")
        return render(request, "contacto.html", {"form": form})

# -------------------------
# ASISTENCIA A EVENTOS
# -------------------------
class AsistenciaView(LoginRequiredMixin, View):
    def get(self, request, evento_id):
        evento = get_object_or_404(Eventos, id=evento_id)
        form = AsistenciaEventoForm()
        asistentes = AsistenciaEvento.objects.filter(evento=evento)\
            .select_related("socio").order_by("-fecha_registro")
        return render(request, "asistencia.html", {
            "evento": evento,
            "asistentes": asistentes,
            "form": form
        })

    def post(self, request, evento_id):
        evento = get_object_or_404(Eventos, id=evento_id)
        form = AsistenciaEventoForm(request.POST)
        if form.is_valid():
            socio = form.cleaned_data['socio']
            if AsistenciaEvento.objects.filter(evento=evento, socio=socio).exists():
                messages.info(request, "¡Ya estabas inscrito en este evento!")
            else:
                AsistenciaEvento.objects.create(evento=evento, socio=socio)
                messages.success(request, "¡Apuntado correctamente!")
            return redirect("asistencia", evento_id=evento.id)
        messages.error(request, "Por favor corrige los errores del formulario.")
        return render(request, "asistencia.html", {"evento": evento, "form": form})


# -------------------------
# LISTA DE ASISTENTES (ADMIN)
# -------------------------
class ListaAsistentesView(UserPassesTestMixin, ListView):
    model = AsistenciaEvento
    template_name = "lista_asistentes.html"
    context_object_name = "asistentes"

    def test_func(self):
        return is_moderador_o_gestor(self.request.user)

    def get_queryset(self):
        evento_id = self.kwargs['evento_id']
        return AsistenciaEvento.objects.filter(evento_id=evento_id)\
            .select_related('socio').order_by('socio__nombre')

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
        return is_moderador_o_gestor(self.request.user)

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
        return is_moderador_o_gestor(self.request.user)

    def get_queryset(self):
        return Contacto.objects.select_related('socio').all().order_by('-fecha_envio')

class EditarSocioView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Gestor").exists()

    def get(self, request, socio_id):
        socio = get_object_or_404(Socio, id=socio_id)
        form = SocioForm(instance=socio)
        return render(request, "editar_socio.html", {"form": form, "socio": socio})

    def post(self, request, socio_id):
        socio = get_object_or_404(Socio, id=socio_id)
        form = SocioForm(request.POST, instance=socio)
        if form.is_valid():
            form.save()
            messages.success(request, "Socio actualizado correctamente.")
            return redirect("detalle_socio", socio_id=socio.id)
        return render(request, "editar_socio.html", {"form": form, "socio": socio})

class EditarAsistentesView(UserPassesTestMixin, View):
    def test_func(self):
        # Solo gestores pueden acceder
        return self.request.user.groups.filter(name="Gestor").exists()

    def get(self, request, evento_id):
        evento = get_object_or_404(Eventos, id=evento_id)
        asistentes = AsistenciaEvento.objects.filter(evento=evento).select_related("socio")
        form = AsistenciaEventoForm()  # Form para agregar un nuevo asistente
        return render(request, "editar_asistentes.html", {
            "evento": evento,
            "asistentes": asistentes,
            "form": form
        })

    def post(self, request, evento_id):
        evento = get_object_or_404(Eventos, id=evento_id)
        form = AsistenciaEventoForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']  # obtener email del formulario
            try:
                socio = Socio.objects.get(email=email)
                # Evitar duplicados
                if not AsistenciaEvento.objects.filter(evento=evento, socio=socio).exists():
                    AsistenciaEvento.objects.create(evento=evento, socio=socio)
                    messages.success(request, "Asistente añadido correctamente.")
                else:
                    messages.info(request, "¡Este socio ya está inscrito en el evento!")
            except Socio.DoesNotExist:
                messages.error(request, "No existe ningún socio con ese email.")

            return redirect("editar_asistentes", evento_id=evento.id)

        # Si hay errores en el form
        asistentes = AsistenciaEvento.objects.filter(evento=evento).select_related("socio")
        messages.error(request, "Corrige los errores del formulario.")
        return render(request, "editar_asistentes.html", {
            "evento": evento,
            "asistentes": asistentes,
            "form": form
        })


class EditarPagoView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Gestor").exists()

    def get(self, request, pago_id):
        pago = get_object_or_404(Pagos, id=pago_id)
        return render(request, "editar_pago.html", {"pago": pago})

    def post(self, request, pago_id):
        pago = get_object_or_404(Pagos, id=pago_id)
        pago.fecha_pago = request.POST.get("fecha_pago", pago.fecha_pago)
        pago.save()
        messages.success(request, "Pago actualizado correctamente.")
        return redirect(f"{reverse('pagos')}?socio_id={pago.socio.id}")
