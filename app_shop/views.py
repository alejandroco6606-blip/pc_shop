from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from inventario.models import Producto, Marca, Proveedor, Categoria
from ventas.models import Cliente, Venta
from inventario.forms import ProductoForm, MarcaForm, ProveedorForm, CategoriaForm
from app_shop.forms import CustomUserCreationForm, UserEditForm
from ventas.forms import ClienteForm, VentaForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


def registro(request):
    if request.method == 'POST':
        # Reutilizamos el formulario seguro que ya creaste
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Iniciar sesión automáticamente después de registrarse
            login(request, user)
            return redirect('inventario:lista_productos')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


# Vista (Read) y (Create) combinadas
@login_required
def lista_productos(request):
    # --- 1. LÓGICA DE CREAR (POST) ---
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_productos')
    else:
        form = ProductoForm()

    # --- 2. LÓGICA DE LISTAR Y BUSCAR (GET) ---
    # Obtenemos TODOS los productos, los más nuevos primero
    productos_list = Producto.objects.all().order_by('-id')

    # Filtramos si hay búsqueda
    busqueda = request.GET.get("buscar")
    if busqueda:
        productos_list = productos_list.filter(
            Q(nombre__icontains=busqueda) |
            Q(marca__nombre__icontains=busqueda) |
            Q(categoria__nombre__icontains=busqueda)
        ).distinct()

    # --- 3. LÓGICA DE PAGINACIÓN ---
    # Aquí defines cuántos productos por página quieres. Probemos con 5 para empezar.
    paginator = Paginator(productos_list, 5) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- 4. ENVIAR A LA PLANTILLA ---
    return render(request, 'productos/lista_productos.html', {
        'productos': page_obj,  # 'productos' ahora es SOLO la página actual
        'form': form,
    })

# --- VISTA DE CREAR (Se mantiene por estructura) ---
# Esta vista ahora puede ser un simple render
# o redirigir a la principal si prefieres.
# La dejaremos funcional por si quieres acceder a /crear/ directamente.
@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_productos')
    else:
        form = ProductoForm()
    # Apunta al HTML de creación
    return render(request, 'productos/crear_producto.html', {'form': form})

# --- ESTAS VISTAS NO CAMBIAN ---

# Editar producto (Update)
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

# Eliminar producto (Delete)
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

# 2. CREAR Marca (Create)
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

# 3. EDITAR Marca (Update)
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

# 4. ELIMINAR Marca (Delete)
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

# --- VISTAS PARA CATEGORÍA ---
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
@login_required
# --- VISTAS PARA CLIENTES ---
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
def lista_usuarios(request):
    usuarios_list = User.objects.all().order_by('-id')
    busqueda = request.GET.get('buscar')
    if busqueda:
        usuarios_list = usuarios_list.filter(
            Q(username__icontains=busqueda) |
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda)
        ).distinct()
    paginator = Paginator(usuarios_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': page_obj})

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UserEditForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form})

@login_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})

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
            venta = form.save(commit=False) # Pausamos el guardado un momento
            venta.vendedor = request.user   # Asignamos el usuario logueado como vendedor
            venta.save()                    # Ahora sí guardamos definitivamente (se calcula el total solo)
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
            form.save() # El método save() del modelo recalculará el total automáticamente
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
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})