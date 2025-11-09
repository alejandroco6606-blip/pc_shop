from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from inventario.models import Producto, Marca, Proveedor, Categoria
from inventario.forms import ProductoForm, MarcaForm, ProveedorForm, CategoriaForm
from django.core.paginator import Paginator
from django.db.models import Q


@login_required
def lista_productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_productos')
    else:
        form = ProductoForm()

    productos_list = Producto.objects.all().order_by('-id')
    busqueda = request.GET.get('buscar')
    if busqueda:
        productos_list = productos_list.filter(
            Q(nombre__icontains=busqueda) |
            Q(marca__nombre__icontains=busqueda) |
            Q(categoria__nombre__icontains=busqueda)
        ).distinct()

    paginator = Paginator(productos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'productos/lista_productos.html', {'productos': page_obj, 'form': form})


@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})


@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar_producto.html', {'form': form})


@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})


@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('inventario:lista_productos')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})


@login_required
def lista_marcas(request):
    marcas_list = Marca.objects.all().order_by('-id')
    busqueda = request.GET.get('buscar')
    if busqueda:
        marcas_list = marcas_list.filter(nombre__icontains=busqueda)
    paginator = Paginator(marcas_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'marcas/lista_marcas.html', {'marcas': page_obj})


@login_required
def crear_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_marcas')
    else:
        form = MarcaForm()
    return render(request, 'marcas/crear_marca.html', {'form': form})


@login_required
def editar_marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_marcas')
    else:
        form = MarcaForm(instance=marca)
    return render(request, 'marcas/editar_marca.html', {'form': form})


@login_required
def eliminar_marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        marca.delete()
        return redirect('inventario:lista_marcas')
    return render(request, 'marcas/eliminar_marca.html', {'marca': marca})


@login_required
def lista_proveedores(request):
    proveedores_list = Proveedor.objects.all().order_by('-id')
    busqueda = request.GET.get('buscar')
    if busqueda:
        proveedores_list = proveedores_list.filter(nombre__icontains=busqueda)
    paginator = Paginator(proveedores_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'proveedores/lista_proveedores.html', {'proveedores': page_obj})


@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/crear_proveedor.html', {'form': form})


@login_required
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/editar_proveedor.html', {'form': form})


@login_required
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('inventario:lista_proveedores')
    return render(request, 'proveedores/eliminar_proveedor.html', {'proveedor': proveedor})


@login_required
def lista_categorias(request):
    categorias_list = Categoria.objects.all().order_by('-id')
    busqueda = request.GET.get('buscar')
    if busqueda:
        categorias_list = categorias_list.filter(nombre__icontains=busqueda)
    paginator = Paginator(categorias_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'categorias/lista_categorias.html', {'categorias': page_obj})


@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/crear_categoria.html', {'form': form})


@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/editar_categoria.html', {'form': form})


@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('inventario:lista_categorias')
    return render(request, 'categorias/eliminar_categoria.html', {'categoria': categoria})
from django.shortcuts import render

# Create your views here.
