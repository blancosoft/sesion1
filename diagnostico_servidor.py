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
