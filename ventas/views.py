from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ventas.models import Venta, Cliente
from inventario.models import Producto
from ventas.forms import VentaForm, ClienteForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q


def registro(request):
    if request.method == 'POST':
        from app_shop.forms import CustomUserCreationForm
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inventario:lista_productos')
    else:
        from app_shop.forms import CustomUserCreationForm
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


@login_required
def lista_ventas(request):
    ventas_list = Venta.objects.all().order_by('-fecha')
    busqueda = request.GET.get('buscar')
    if busqueda:
        ventas_list = ventas_list.filter(
            Q(cliente__nombre__icontains=busqueda) |
            Q(vendedor__username__icontains=busqueda)
        ).distinct()
    paginator = Paginator(ventas_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ventas/lista_ventas.html', {'ventas': page_obj})


@login_required
def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.vendedor = request.user
            venta.save()
            return redirect('ventas:lista_ventas')
    else:
        form = VentaForm()
    return render(request, 'ventas/crear_venta.html', {'form': form})


@login_required
def editar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('ventas:lista_ventas')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'ventas/editar_venta.html', {'form': form, 'venta': venta})


@login_required
def eliminar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('ventas:lista_ventas')
    return render(request, 'ventas/eliminar_venta.html', {'venta': venta})


@login_required
def lista_clientes(request):
    clientes_list = Cliente.objects.all().order_by('-id')
    busqueda = request.GET.get('buscar')
    if busqueda:
        clientes_list = clientes_list.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellido__icontains=busqueda) |
            Q(rut__icontains=busqueda)
        ).distinct()
    paginator = Paginator(clientes_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'clientes/lista_clientes.html', {'clientes': page_obj})


@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ventas:lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear_cliente.html', {'form': form})


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('ventas:lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_cliente.html', {'form': form})


@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ventas:lista_clientes')
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})


@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})


@login_required
def detalle_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'clientes/detalle_cliente.html', {'cliente': cliente})


@login_required
def detalle_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    return render(request, 'ventas/detalle_venta.html', {'venta': venta})
from django.shortcuts import render

# Create your views here.
