# Sesión 1 — Sistemas Expertos e IA
## Solución de talleres

---

## Taller Analítico 1: Lógica Proposicional (Crédito Hipotecario Plus)

### Texto fuente
> "Un cliente es elegible para el crédito Hipotecario Plus si sus ingresos anuales superan los 50,000 USD y tiene un historial crediticio 'Excelente'. Sin embargo, si el cliente tiene deudas activas superiores a 10,000 USD, no será elegible bajo ninguna circunstancia, a menos que presente un avalista."

### 1. Variables (Hechos) que el sistema debe pedir al usuario

| Variable | Tipo | Descripción |
|---|---|---|
| `ingresos_anuales` | numérico (USD) | Ingresos anuales del cliente |
| `historial_crediticio` | categórico | Ej. "Excelente", "Bueno", "Regular" |
| `deuda_activa` | numérico (USD) | Monto total de deudas activas |
| `tiene_avalista` | booleano | Si el cliente presenta un avalista |

### 2. Formalización en lógica proposicional

Definiendo:
- **A** = ingresos_anuales > 50000
- **B** = historial_crediticio = "Excelente"
- **C** = deuda_activa > 10000
- **D** = tiene_avalista = Verdadero

La regla de rechazo (C ∧ ¬D) tiene **precedencia absoluta** sobre la regla de aprobación (A ∧ B): el enunciado "no será elegible bajo ninguna circunstancia" indica que esta condición anula cualquier otra, salvo la excepción del avalista.

**Elegibilidad = (A ∧ B) ∧ ¬(C ∧ ¬D)**

### 3. Reglas de Producción (SI... ENTONCES...)

```
R1 (Rechazo absoluto — máxima precedencia):
   SI deuda_activa > 10000 Y NO tiene_avalista
   ENTONCES elegible = FALSO
   [Esta regla se evalúa primero y, si se cumple, detiene el proceso]

R2 (Aprobación):
   SI ingresos_anuales > 50000 Y historial_crediticio = "Excelente"
   ENTONCES elegible = VERDADERO

R3 (Rechazo por defecto — fallback):
   SI ninguna de las anteriores se cumple
   ENTONCES elegible = FALSO (no cumple ingresos/historial)
```

**Nota de ingeniería del conocimiento:** R1 debe evaluarse *antes* que R2 en el motor de inferencia (orden de precedencia), porque la deuda sin avalista descalifica al cliente "bajo ninguna circunstancia", incluso si cumple ingresos e historial. Si el cliente tiene deuda alta pero SÍ presenta avalista, la excepción neutraliza a R1 y el sistema pasa a evaluar R2 con normalidad.

---

## Taller de Laboratorio: Sistema de Diagnóstico IT (HelpDesk)

Para que la Memoria de Trabajo sea editable sin tocar el código, los hechos se separan en un archivo `servidor_estado.json`. Basta con cambiar sus valores y volver a ejecutar el script para que el motor tome caminos distintos.

**`servidor_estado.json`**
```json
{
    "cpu_uso": 45,
    "memoria_libre": 60,
    "ping_respuesta": 25,
    "temperatura": 55,
    "ventilador_encendido": true
}
```

**`diagnostico_servidor.py`**
```python
# ============================================================
# SISTEMA EXPERTO — DIAGNÓSTICO DE SERVIDOR (HelpDesk IT)
# Hechos cargados dinámicamente desde un archivo JSON
# ============================================================
import json
import os

RUTA_JSON = os.path.join(os.path.dirname(__file__), "servidor_estado.json")


# 1. MEMORIA DE TRABAJO (Base de Hechos) — se lee desde el JSON
def cargar_hechos(ruta=RUTA_JSON):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


# 2. BASE DE REGLAS Y MOTOR DE INFERENCIA
def diagnosticar_servidor(hechos):
    diagnosticos = []

    # --- Regla 1 (precedencia alta): Estado CRÍTICO por sobrecalentamiento ---
    if hechos["temperatura"] > 80 and not hechos["ventilador_encendido"]:
        diagnosticos.append(
            "CRÍTICO: Sobrecalentamiento sin ventilación. Riesgo de apagado "
            "por hardware. Apagar el equipo de inmediato."
        )
    elif hechos["temperatura"] > 80 and hechos["ventilador_encendido"]:
        diagnosticos.append(
            "ADVERTENCIA: Temperatura alta pero el ventilador está activo. "
            "Monitorear de cerca."
        )

    # --- Regla 2: Estado CRÍTICO por saturación de recursos ---
    if hechos["cpu_uso"] > 90 and hechos["memoria_libre"] < 10:
        diagnosticos.append(
            "CRÍTICO: CPU saturada y memoria casi agotada. Posible caída "
            "inminente del servicio."
        )
    elif hechos["cpu_uso"] > 75 or hechos["memoria_libre"] < 20:
        diagnosticos.append(
            "ADVERTENCIA: Uso elevado de recursos (CPU y/o memoria). "
            "Revisar procesos activos."
        )

    # --- Regla 3: Estado de red ---
    if hechos["ping_respuesta"] > 500:
        diagnosticos.append(
            "CRÍTICO: Latencia de red muy alta (>500ms). Posible caída de "
            "conectividad."
        )
    elif hechos["ping_respuesta"] > 150:
        diagnosticos.append(
            "ADVERTENCIA: Latencia de red por encima de lo normal."
        )

    # --- Regla por defecto (Fallback): todo en orden ---
    if not diagnosticos:
        return ["NORMAL: Todos los parámetros dentro de rangos aceptables."]

    return diagnosticos


# 3. EJECUCIÓN
if __name__ == "__main__":
    hechos = cargar_hechos()

    print("=== Hechos cargados desde servidor_estado.json ===")
    for clave, valor in hechos.items():
        print(f"  {clave}: {valor}")

    print("\n=== Diagnóstico ===")
    for linea in diagnosticar_servidor(hechos):
        print("-", linea)
```

### Explicación del diseño

1. **`servidor_estado.json`**: Base de Hechos separada del código. Contiene las 5 métricas técnicas y se puede editar directamente (con cualquier editor de texto) sin tocar el motor de inferencia.
2. **`cargar_hechos()`**: lee el JSON y lo convierte en un diccionario de Python (Hash Map) → acceso O(1), tal como se explicó en la sesión.
3. **`diagnosticar_servidor(hechos)`**: contiene 3 bloques de reglas anidadas (`if/elif`) que combinan operadores `and`/`or`, cada uno con una condición crítica y una de advertencia.
4. **Regla por defecto (fallback)**: si ninguna condición se dispara, se retorna un diagnóstico "NORMAL", igual que en el ejemplo del motor de crédito.
5. **Cobertura de ramas (punto 4 del taller)**: en vez de modificar el diccionario en memoria, se cambian los valores en `servidor_estado.json` y se vuelve a ejecutar `python diagnostico_servidor.py`. Esto obliga al motor a tomar caminos distintos sin recompilar ni editar el script.

### Pruebas de cobertura (cambiando solo el JSON)

| Contenido del JSON | Diagnóstico resultante |
|---|---|
| `temperatura: 55, ventilador_encendido: true` (valores originales) | `NORMAL: Todos los parámetros dentro de rangos aceptables.` |
| `temperatura: 88, ventilador_encendido: false` | `CRÍTICO: Sobrecalentamiento sin ventilación...` |
| `cpu_uso: 82, memoria_libre: 15, ping_respuesta: 200` | `ADVERTENCIA: Uso elevado de recursos...` + `ADVERTENCIA: Latencia de red por encima de lo normal.` |

Estos tres casos fueron verificados ejecutando el script con distintas versiones del JSON, confirmando que el motor de inferencia responde correctamente a cada cambio.
