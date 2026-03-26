from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid
import httpx

app = FastAPI(
    title="SistemaRep API",
    description="API para gestión de reparación y entrega de equipos",
    version="1.0.0"
)

# ── Credenciales Trello ───────────────────────────────────────────────────────
TRELLO_API_KEY = "7884cda81d06fd9b0e3f1eecd02b13c6"
TRELLO_TOKEN   = "ATTA8359ffbf96f15caa7994100e0b3caa9162bf4d356d8b056f0cd5a1bc363bb77687F08603"
TRELLO_LIST_ID = "69a34b8346e8b7122a205195"  # Lista "Must Have"

# ── Base de datos en memoria ──────────────────────────────────────────────────
equipos_db: dict = {}

# ── Modelos ───────────────────────────────────────────────────────────────────

class EquipoEntrada(BaseModel):
    cliente_nombre: str = Field(..., min_length=2)
    cliente_telefono: str = Field(..., min_length=8)
    marca: str = Field(..., min_length=1)
    modelo: str = Field(..., min_length=1)
    numero_serie: str = Field(..., min_length=3)
    falla_reportada: str = Field(..., min_length=5)
    caracteristicas: Optional[str] = None

class EstadoActualizacion(BaseModel):
    estado: str = Field(..., description="recibido | en_diagnostico | en_reparacion | listo | entregado")
    tecnico: Optional[str] = None

class EquipoRespuesta(BaseModel):
    id: str
    cliente_nombre: str
    cliente_telefono: str
    marca: str
    modelo: str
    numero_serie: str
    falla_reportada: str
    caracteristicas: Optional[str]
    estado: str
    tecnico: Optional[str]
    fecha_ingreso: str
    fecha_actualizacion: str
    trello_card_id: Optional[str] = None

# ── Funciones Trello ──────────────────────────────────────────────────────────

async def crear_tarjeta_trello(equipo: dict) -> Optional[str]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.trello.com/1/cards",
                params={
                    "key": TRELLO_API_KEY,
                    "token": TRELLO_TOKEN,
                    "idList": TRELLO_LIST_ID,
                    "name": f"[{equipo['id']}] {equipo['marca']} {equipo['modelo']} — {equipo['cliente_nombre']}",
                    "desc": (
                        f"**Cliente:** {equipo['cliente_nombre']}\n"
                        f"**Teléfono:** {equipo['cliente_telefono']}\n"
                        f"**Serie:** {equipo['numero_serie']}\n"
                        f"**Falla:** {equipo['falla_reportada']}\n"
                        f"**Características:** {equipo.get('caracteristicas') or 'N/A'}\n"
                        f"**Estado:** {equipo['estado']}\n"
                        f"**Ingreso:** {equipo['fecha_ingreso']}"
                    )
                }
            )
            if response.status_code == 200:
                return response.json().get("id")
    except Exception as e:
        print(f"Error Trello: {e}")
    return None

async def actualizar_tarjeta_trello(card_id: str, equipo: dict):
    try:
        async with httpx.AsyncClient() as client:
            await client.put(
                f"https://api.trello.com/1/cards/{card_id}",
                params={
                    "key": TRELLO_API_KEY,
                    "token": TRELLO_TOKEN,
                    "name": f"[{equipo['id']}] {equipo['marca']} {equipo['modelo']} — {equipo['estado'].upper()}",
                    "desc": (
                        f"**Cliente:** {equipo['cliente_nombre']}\n"
                        f"**Teléfono:** {equipo['cliente_telefono']}\n"
                        f"**Serie:** {equipo['numero_serie']}\n"
                        f"**Falla:** {equipo['falla_reportada']}\n"
                        f"**Estado:** {equipo['estado']}\n"
                        f"**Técnico:** {equipo.get('tecnico') or 'Sin asignar'}\n"
                        f"**Actualización:** {equipo['fecha_actualizacion']}"
                    )
                }
            )
    except Exception as e:
        print(f"Error Trello: {e}")

# ── Endpoints ─────────────────────────────────────────────────────────────────

ESTADOS_VALIDOS = {"recibido", "en_diagnostico", "en_reparacion", "listo", "entregado"}

@app.get("/", tags=["General"])
def root():
    return {"mensaje": "SistemaRep API v1.0.0 funcionando correctamente"}


@app.post("/equipos", response_model=EquipoRespuesta, status_code=201, tags=["Equipos"])
async def registrar_equipo(equipo: EquipoEntrada):
    for e in equipos_db.values():
        if e["numero_serie"] == equipo.numero_serie:
            raise HTTPException(status_code=400, detail=f"Ya existe un equipo con número de serie '{equipo.numero_serie}'")

    equipo_id = str(uuid.uuid4())[:8].upper()
    ahora = datetime.now().isoformat()

    nuevo_equipo = {
        "id": equipo_id,
        "cliente_nombre": equipo.cliente_nombre,
        "cliente_telefono": equipo.cliente_telefono,
        "marca": equipo.marca,
        "modelo": equipo.modelo,
        "numero_serie": equipo.numero_serie,
        "falla_reportada": equipo.falla_reportada,
        "caracteristicas": equipo.caracteristicas,
        "estado": "recibido",
        "tecnico": None,
        "fecha_ingreso": ahora,
        "fecha_actualizacion": ahora,
        "trello_card_id": None,
    }

    card_id = await crear_tarjeta_trello(nuevo_equipo)
    nuevo_equipo["trello_card_id"] = card_id
    equipos_db[equipo_id] = nuevo_equipo
    return nuevo_equipo


@app.get("/equipos", response_model=list[EquipoRespuesta], tags=["Equipos"])
def listar_equipos(estado: Optional[str] = None):
    if estado:
        if estado not in ESTADOS_VALIDOS:
            raise HTTPException(status_code=400, detail=f"Estado inválido.")
        return [e for e in equipos_db.values() if e["estado"] == estado]
    return list(equipos_db.values())


@app.get("/equipos/{equipo_id}", response_model=EquipoRespuesta, tags=["Equipos"])
def consultar_equipo(equipo_id: str):
    equipo = equipos_db.get(equipo_id.upper())
    if not equipo:
        raise HTTPException(status_code=404, detail=f"Equipo '{equipo_id}' no encontrado")
    return equipo


@app.patch("/equipos/{equipo_id}/estado", response_model=EquipoRespuesta, tags=["Equipos"])
async def actualizar_estado(equipo_id: str, actualizacion: EstadoActualizacion):
    equipo = equipos_db.get(equipo_id.upper())
    if not equipo:
        raise HTTPException(status_code=404, detail=f"Equipo '{equipo_id}' no encontrado")

    if actualizacion.estado not in ESTADOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Use: {', '.join(ESTADOS_VALIDOS)}")

    equipo["estado"] = actualizacion.estado
    equipo["fecha_actualizacion"] = datetime.now().isoformat()
    if actualizacion.tecnico:
        equipo["tecnico"] = actualizacion.tecnico

    if equipo.get("trello_card_id"):
        await actualizar_tarjeta_trello(equipo["trello_card_id"], equipo)

    return equipo
