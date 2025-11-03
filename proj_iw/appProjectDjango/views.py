from django.shortcuts import render, get_object_or_404
from .models import Socio, Eventos, Cuotas, Merchandising
from django.contrib.auth.decorators import user_passes_test

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

# Vista de registros
def registros(request):
    return render(request, 'registro.html')

def cuotas(request):
    cuotas = Cuotas.objects.all()
    return render(request, 'cuotas.html', {'cuotas': cuotas})