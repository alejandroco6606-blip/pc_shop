# 🖥️ PC_Shop: Sistema de Gestión de Inventario y Ventas

**PC_Shop** es una aplicación web interna construida con Django, diseñada para reemplazar la gestión manual de inventario con una solución centralizada, segura y eficiente. Permite a los vendedores gestionar productos, clientes y registrar ventas en tiempo real.

Este proyecto fue desarrollado cumpliendo con una rúbrica que exigía un CRUD completo para múltiples modelos, relaciones de base de datos, autenticación, lógica de negocio y una arquitectura organizada en múltiples aplicaciones.

## ✨ Funcionalidades Principales

El sistema cuenta con 4 módulos principales:

### 1. Seguridad y Autenticación
* **Autenticación Completa:** Sistema de **Login**, **Logout** y **Registro** de usuarios (vendedores) usando `django.contrib.auth`.
* **Vistas Protegidas:** Toda la aplicación es privada. Ningún módulo es accesible sin haber iniciado sesión (`@login_required`).
* **Trazabilidad:** El sistema registra qué vendedor (`request.user`) realiza cada venta.
* **Permisos Básicos:** El módulo de administración de usuarios del sistema solo es visible para `is_staff` (administradores).

### 2. App: `app_shop` (Inventario y Clientes)
* **CRUD de Productos:** Gestión completa de productos.
* **CRUDs de Soporte:** Gestión independiente de `Marcas`, `Categorías`, `Proveedores` y `Clientes`.
* **Relaciones:** El modelo `Producto` está conectado vía `ForeignKey` a sus tablas de soporte (Marca, Categoría, Proveedor).
* **Vista de Detalle:** Página de "Ficha Técnica" para cada producto.

### 3. App: `app_ventas` (Transacciones)
* **CRUD de Ventas:** Sistema para registrar, editar y eliminar transacciones.
* **Lógica de Negocio (Backend):**
    1.  **Cálculo Automático de Total:** El total de la venta (`precio * cantidad`) se calcula automáticamente en el backend (sobrescribiendo el método `.save()` del modelo) para garantizar la integridad de los datos.
    2.  **Asignación de Vendedor:** La vista `crear_venta` asigna automáticamente al usuario logueado (`request.user`) como el vendedor.

### 4. Funcionalidades Avanzadas de Listado
* **Buscador (Productos):** Implementado con `Q objects` de Django para permitir búsquedas por nombre, marca o categoría.
* **Paginación (Productos):** Implementada con `Paginator` de Django para mostrar las listas de forma ordenada y rápida (de 5 en 5).

## 🏛️ Arquitectura del Proyecto

El proyecto está organizado en una arquitectura multi-app para separar responsabilidades, como lo exigen las buenas prácticas de Django:
* `pc_shop/`: El proyecto principal (configuración, `settings.py`, `urls.py` principales).
* `app_shop/`: App que gestiona el inventario, catálogo y clientes.
* `app_ventas/`: App dedicada exclusivamente a la lógica transaccional (Ventas).



## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.13, Django 5.2.8
* **Base de Datos:** MySQL
* **Frontend:** HTML5, CSS3, Bootstrap 5.3
* **Dependencias Clave:** `mysqlclient`, `python-dotenv`

---

## 🚀 Instalación y Ejecución Local

Sigue estos pasos para levantar el proyecto en un entorno de desarrollo.

### 1. Prerrequisitos
* Tener Python 3.13+ instalado.
* Tener un servidor MySQL funcionando.

### 2. Clonar el Repositorio
```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd pc_shop