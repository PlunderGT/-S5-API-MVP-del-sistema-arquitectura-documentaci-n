# Requirements & Product Backlog — SistemaRep

## 1. Enlace al Tablero Trello

🗂️ **Tablero oficial del proyecto:**  
👉 [https://trello.com/b/PLACEHOLDER-SISTEMAREP/sistemarep-backlog](https://trello.com/b/PLACEHOLDER-SISTEMAREP/sistemarep-backlog)

> **Nota:** Reemplazar con la URL real de tu tablero Trello.

---

## 2. Backlog de Historias de Usuario

| # | Historia de Usuario | Prioridad |
|---|---------------------|-----------|
| US-01 | Como recepcionista, quiero registrar un cliente con sus datos de contacto, para tener su ficha disponible | **Must** |
| US-02 | Como recepcionista, quiero registrar un equipo con marca, modelo y número de serie, para documentar el activo recibido | **Must** |
| US-03 | Como sistema, quiero generar una etiqueta con QR al registrar un equipo, para identificarlo físicamente | **Must** |
| US-04 | Como técnico, quiero ver mis órdenes asignadas con su estado, para organizar mi trabajo diario | **Must** |
| US-05 | Como técnico, quiero actualizar el estado de una orden (recibido / en reparación / listo), para reflejar el avance real | **Must** |
| US-06 | Como sistema, quiero enviar un email al cliente cuando su equipo esté listo, para avisarle sin llamadas manuales | **Should** |
| US-07 | Como recepcionista, quiero registrar la entrega con firma digital, para tener respaldo de que el equipo fue devuelto | **Should** |
| US-08 | Como administrador, quiero ver un reporte de órdenes por técnico y estado, para supervisar la productividad | **Could** |

---

## 3. Criterios de Aceptación

### US-02 — Registro de Equipo

#### Criterio 1 — Registro exitoso
```
Given que el recepcionista está en el formulario de nuevo equipo
  And ha seleccionado un cliente existente
When completa marca, modelo, número de serie y falla reportada
  And hace clic en "Guardar"
Then el sistema crea la orden con estado "recibido"
  And muestra el ID generado
```

#### Criterio 2 — Número de serie duplicado
```
Given que existe un equipo con número de serie "SN-2024-001"
When se intenta registrar otro equipo con el mismo número de serie
Then el sistema responde con error 400
  And muestra: "Ya existe un equipo con este número de serie"
```

---

### US-05 — Actualización de Estado

#### Criterio 1 — Cambio de estado válido
```
Given que existe la orden con ID "A1B2C3D4" en estado "recibido"
When el técnico envía PATCH /equipos/A1B2C3D4/estado con {"estado": "en_reparacion"}
Then el sistema actualiza el estado
  And registra la fecha y hora del cambio
  And retorna el equipo actualizado con código 200
```

#### Criterio 2 — Estado inválido
```
Given que existe la orden con ID "A1B2C3D4"
When se envía un estado que no existe, por ejemplo "arreglado"
Then el sistema responde con error 400
  And muestra los estados válidos permitidos
```

---

## 4. MVP Rationale

Las historias clasificadas como **Must** (US-01 a US-05) conforman el núcleo del MVP porque representan el flujo mínimo indispensable para operar digitalmente: recibir un equipo, documentarlo, identificarlo con una etiqueta, asignarlo a un técnico y registrar el avance. Sin estos cinco elementos el sistema no aporta valor real sobre un proceso manual. Las historias **Should** (US-06 y US-07) mejoran la experiencia pero el taller puede operar sin ellas en fase piloto. La historia **Could** (US-08) se posterga porque requiere datos acumulados para ser útil y no impacta la operación diaria en las primeras semanas.

---

*Documento versionado — v1.0 — Febrero 2026*
