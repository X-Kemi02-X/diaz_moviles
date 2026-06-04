# Diaz Moviles - API Backend

Backend Django REST para tienda de equipos móviles.

## 🌐 URL de Producción

```
https://diaz-moviles.uaeftt-ute.site
```

## 🔐 Credenciales de Prueba

| Rol | Usuario | Contraseña |
|-----|---------|------------|
| Admin | `admin` | `admin123` |
| Cliente | `cliente` | `cliente123` |

## Stack
- Python 3.12, Django 6.0, DRF 3.17
- PostgreSQL, JWT (SimpleJWT)
- Gunicorn, Nginx

## Instalación local

```bash
# Clonar
git clone <repo-url>
cd diaz_moviles

# Activar entorno
.venv\Scripts\Activate.ps1          # Windows
source .venv/bin/activate            # Linux/Mac

# Instalar dependencias
uv sync

# Crear BD (PostgreSQL)
psql -U postgres -f script.sql

# Migrar
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos de prueba
python seed_data.py

# Iniciar servidor
python manage.py runserver
```

## Endpoints

### Auth
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/token/` | Login (obtener JWT) |
| POST | `/api/token/refresh/` | Refrescar token |

### Catálogo (admin: CRUD completo / usuario: solo lectura)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET/POST | `/api/marcas/` | Listar / Crear marca |
| GET/PUT/DELETE | `/api/marcas/{id}/` | Detalle / Actualizar / Eliminar |
| GET/POST | `/api/categorias/` | Listar / Crear categoría |
| GET/PUT/DELETE | `/api/categorias/{id}/` | Detalle / Actualizar / Eliminar |
| GET/POST | `/api/productos/` | Listar / Crear producto |
| GET/PUT/DELETE | `/api/productos/{id}/` | Detalle / Actualizar / Eliminar |
| GET/POST | `/api/proveedores/` | Listar / Crear proveedor |
| GET/PUT/DELETE | `/api/proveedores/{id}/` | Detalle / Actualizar / Eliminar |

### Clientes
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET/POST | `/api/clientes/` | Listar / Crear cliente |
| GET/PUT/DELETE | `/api/clientes/{id}/` | Detalle / Actualizar / Eliminar |

### Ventas
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET/POST | `/api/ventas/` | Listar / Crear venta |
| GET/PUT/PATCH/DELETE | `/api/ventas/{id}/` | Detalle / Actualizar / Eliminar |
| GET/POST | `/api/detalles-venta/` | Listar / Crear detalle |
| GET/DELETE | `/api/detalles-venta/{id}/` | Detalle / Eliminar |

### Filtros y búsqueda
```
?search=palabra         # Búsqueda general
?marca=1                # Filtrar por marca
?categoria=2            # Filtrar por categoría
?activo=true            # Filtrar por estado
?precio_min=100         # Precio mínimo
?precio_max=1000        # Precio máximo
?ordering=-precio       # Ordenar (descendente)
?ordering=nombre        # Ordenar (ascendente)
?page=2                 # Paginación
?page_size=20           # Tamaño de página
```

## Modelos de datos (JSON)

### Marca
```json
{
  "id": 1,
  "nombre": "Samsung",
  "descripcion": "Electrónica coreana",
  "pais_origen": "Corea del Sur",
  "activo": true,
  "fecha_creacion": "2026-06-03T00:00:00Z",
  "fecha_actualizacion": "2026-06-03T00:00:00Z"
}
```

### Producto
```json
{
  "id": 1,
  "nombre": "Galaxy S24",
  "marca": 1,
  "categoria": 1,
  "modelo": "S24",
  "precio": "899.99",
  "stock": 15,
  "descripcion": "",
  "especificaciones": null,
  "imagen_url": "",
  "activo": true,
  "marca_nombre": "Samsung",
  "categoria_nombre": "Smartphone",
  "fecha_creacion": "2026-06-03T00:00:00Z",
  "fecha_actualizacion": "2026-06-03T00:00:00Z"
}
```

### Cliente
```json
{
  "id": 1,
  "nombre": "Juan",
  "apellido": "Pérez",
  "cedula": "1234567890",
  "email": "juan@email.com",
  "telefono": "0991234567",
  "direccion": "",
  "activo": true,
  "fecha_registro": "2026-06-03T00:00:00Z",
  "fecha_actualizacion": "2026-06-03T00:00:00Z"
}
```

### Venta con detalles
```json
{
  "id": 1,
  "cliente": 1,
  "usuario": 1,
  "fecha": "2026-06-03T00:00:00Z",
  "total": "1199.98",
  "estado": "completada",
  "metodo_pago": "tarjeta",
  "observacion": "",
  "detalles": [
    {
      "id": 1,
      "venta": 1,
      "producto": 1,
      "cantidad": 1,
      "precio_unitario": "899.99",
      "subtotal": "899.99",
      "producto_nombre": "Galaxy S24"
    }
  ],
  "cliente_nombre": "Juan",
  "usuario_nombre": "admin"
}
```

## Uso con Postman

### Local
1. Importar `Proyecto-MovilesD.postman_collection.json`
2. Crear environment con variable `base_url = http://127.0.0.1:8000`
3. Ejecutar **Login** → el token se guarda automáticamente
4. Probar cualquier endpoint

### Producción
1. Importar `Proyecto-MovilesD-Produccion.postman_collection.json`
2. La variable `base_url` ya apunta a `https://diaz-moviles.uaeftt-ute.site`
3. Ejecutar **Login** → el token se guarda automáticamente
4. Probar cualquier endpoint

## Ejemplos con curl

### Local
```bash
# Login
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Listar productos (con token)
curl -H "Authorization: Bearer <token>" \
  http://127.0.0.1:8000/api/productos/?search=galaxy

# Crear marca (admin)
curl -X POST http://127.0.0.1:8000/api/marcas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"nombre":"Google","pais_origen":"Estados Unidos"}'
```

### Producción
```bash
# Login
curl -X POST https://diaz-moviles.uaeftt-ute.site/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Listar productos
curl -H "Authorization: Bearer <token>" \
  https://diaz-moviles.uaeftt-ute.site/api/productos/

# Crear cliente
curl -X POST https://diaz-moviles.uaeftt-ute.site/api/clientes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"nombre":"Ana","apellido":"Martínez","cedula":"1723456789","email":"ana@email.com","telefono":"0995551234"}'
```

## Despliegue

| Recurso | URL |
|---------|-----|
| API Producción | `https://diaz-moviles.uaeftt-ute.site` |
| Admin Django | `https://diaz-moviles.uaeftt-ute.site/admin/` |
| Servidor | DigitalOcean Droplet (Ubuntu 24.04) |
| CI/CD | GitHub Actions → despliegue automático al hacer push a `main` |
