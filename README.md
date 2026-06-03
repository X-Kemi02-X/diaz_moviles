# Diaz Moviles - API Backend

Backend Django REST para tienda de equipos móviles.

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

## Uso con Postman

1. Importar `Proyecto-MovilesD.postman_collection.json`
2. Crear environment con variable `base_url = http://127.0.0.1:8000`
3. Ejecutar **Login** → el token se guarda automáticamente
4. Probar cualquier endpoint

## Ejemplos con curl

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

## Despliegue

Desplegado en DigitalOcean: `https://diaz-moviles.uaeftt-ute.site`

El CI/CD en GitHub Actions despliega automáticamente al hacer push a `main`.
