# 🔧 SistemaRep — API de Reparación y Entrega de Equipos

## Descripción

**SistemaRep** es una API REST para gestionar el ciclo completo de reparación de equipos electrónicos en talleres técnicos: registro de equipos, seguimiento de reparaciones, actualización de estados y consulta de órdenes activas.

## Documentación

| Documento | Descripción |
|-----------|-------------|
| [System Brief](docs/system-brief.md) | Visión, alcance y diagrama de contexto |
| [Requirements](docs/requirements.md) | Historias de usuario y criterios de aceptación |
| [Architecture](docs/architecture.md) | Arquitectura, decisiones técnicas y diagramas |
| [OpenAPI Spec](docs/api/openapi.yaml) | Contrato completo de la API |
| [Tablero Trello](https://trello.com/b/PLACEHOLDER) | Backlog del proyecto |

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Estado de la API |
| `POST` | `/equipos` | Registrar nuevo equipo |
| `GET` | `/equipos` | Listar equipos (con filtro opcional por estado) |
| `GET` | `/equipos/{id}` | Consultar equipo por ID |
| `PATCH` | `/equipos/{id}/estado` | Actualizar estado de reparación |

## Estados del Flujo

```
recibido → en_diagnostico → en_reparacion → listo → entregado
```

## ▶️ Cómo ejecutar la API localmente

### 1. Clonar el repositorio
```bash
git clone https://github.com/PlunderGT/sistemarep.git
cd sistemarep
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la API
```bash
uvicorn main:app --reload
```

### 4. Abrir la documentación interactiva
Abre en el navegador: [http://localhost:8000/docs](http://localhost:8000/docs)

## Ejemplo rápido

### Registrar un equipo
```bash
curl -X POST http://localhost:8000/equipos \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nombre": "Juan García",
    "cliente_telefono": "50212345678",
    "marca": "Dell",
    "modelo": "Inspiron 15",
    "numero_serie": "SN-2024-001",
    "falla_reportada": "No enciende, posible falla en fuente de poder"
  }'
```

### Actualizar estado
```bash
curl -X PATCH http://localhost:8000/equipos/A1B2C3D4/estado \
  -H "Content-Type: application/json" \
  -d '{"estado": "en_reparacion", "tecnico": "Carlos Méndez"}'
```

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Lenguaje | Python 3.10+ |
| Framework | FastAPI 0.110.0 |
| Servidor | Uvicorn |
| Validación | Pydantic v2 |
| Base de datos | En memoria (MVP) |

## Estructura del Repositorio

```
sistemarep/
├── main.py                    ← API ejecutable
├── requirements.txt           ← Dependencias
├── README.md
└── docs/
    ├── system-brief.md
    ├── requirements.md
    ├── architecture.md
    └── api/
        └── openapi.yaml
```

---
*MVP v1.0 — SistemaRep — Ingeniería de Software*
