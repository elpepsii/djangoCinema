from django.shortcuts import render, redirect

# Create your views here.
from .models import Funcion, Peliculas, Ventas
from .forms import FormVenta

import datetime

def index(request):
    funciones = Funcion.objects.all();
    data = {'funciones': funciones}
    return render(request, 'index.html', data)

def ticket(request, id):
    venta = Ventas.objects.get(id=id);
    data = {'venta': venta}
    return render(request, 'ticket.html', data)

def comprar(request, id):
    DESCUENTO = 37
    form = FormVenta()
    form.fields['id_funcion'].inital = id
    if request.method == 'POST':
        form = FormVenta(request.POST)
        if form.is_valid():
            funcion = Funcion.objects.get(id = id)

            cantidad = form.cleanded_data['entradas']
            funcion.asientos_disponibles -= cantidad
            funcion.asientos_vendidos += cantidad
            funcion.save()

            venta = Ventas()
            venta.funcion = funcion
            venta.cliente = form.cleaned_data['cliente']
            venta.entradas = form.cleaned_data['entradas']
            venta.codigo = form.cleaned_data['codigo']
            venta.email = form.cleaned_data['email']
            venta.fecha = datetime.datetime.now()

            descuento = DESCUENTO if venta.codigo != "" else 0
            valor_entrada = funcion.precio
            total_original = venta.entradas * valor_entrada
            total_descuento = total_original * descuento / 100
            total_final = total_original - total_descuento

            venta.total_original = total_original
            venta.total_descuento = total_descuento
            venta.total_final = total_final
            venta.save()

            return redirect('/ticket/' + str(venta.id))

    funcion = Funcion.objects.get(id=id)
    data = {
        'funcion': funcion,
        'form': form
    }
    return render(request, 'comprar.html', data)