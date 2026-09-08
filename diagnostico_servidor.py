# ============================================================
# SISTEMA EXPERTO — DIAGNÓSTICO DE SERVIDOR (HelpDesk IT)
# Hechos cargados dinámicamente desde un archivo JSON
# ============================================================
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

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


class VentanaDiagnostico:
    def __init__(self, raiz):
        # La ventana mantiene los valores editables que alimentan el motor de reglas.
        self.raiz = raiz
        self.raiz.title("Diagnostico de servidor")
        self.raiz.geometry("720x610")
        self.raiz.minsize(620, 520)
        self.raiz.configure(bg="#eef3f7")

        hechos = cargar_hechos()
        self.cpu_uso = tk.DoubleVar(value=hechos["cpu_uso"])
        self.memoria_libre = tk.DoubleVar(value=hechos["memoria_libre"])
        self.ping_respuesta = tk.DoubleVar(value=hechos["ping_respuesta"])
        self.temperatura = tk.DoubleVar(value=hechos["temperatura"])
        self.ventilador_encendido = tk.BooleanVar(
            value=hechos["ventilador_encendido"]
        )

        # Se configura un estilo sencillo para separar parametros, acciones y alertas.
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 22, "bold"),
                         foreground="#17324d", background="#eef3f7")
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10),
                         foreground="#526475", background="#eef3f7")
        estilo.configure("Panel.TLabelframe", background="#ffffff")
        estilo.configure("Panel.TLabelframe.Label", font=("Segoe UI", 11, "bold"),
                         foreground="#17324d", background="#ffffff")

        contenedor = tk.Frame(raiz, bg="#eef3f7", padx=28, pady=22)
        contenedor.pack(fill="both", expand=True)
        ttk.Label(contenedor, text="Diagnostico de servidor",
                  style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Modifica los parametros y ejecuta el motor de reglas para evaluar el estado.",
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(2, 18))

        # Cada barra representa un hecho que el usuario puede modificar.
        panel = ttk.LabelFrame(contenedor, text="Parametros del servidor",
                               style="Panel.TLabelframe", padding=18)
        panel.pack(fill="x")
        self._crear_control(panel, "Uso de CPU", self.cpu_uso, 0, 100, "%")
        self._crear_control(panel, "Memoria libre", self.memoria_libre, 0, 100, "%")
        self._crear_control(panel, "Respuesta de ping", self.ping_respuesta, 0, 1000, " ms")
        self._crear_control(panel, "Temperatura", self.temperatura, 0, 600, " C")

        ttk.Checkbutton(
            panel,
            text="Ventilador encendido",
            variable=self.ventilador_encendido,
            command=self.evaluar,
        ).pack(anchor="w", pady=(10, 0))

        acciones = tk.Frame(contenedor, bg="#eef3f7")
        acciones.pack(fill="x", pady=16)
        ttk.Button(acciones, text="Evaluar estado", command=self.evaluar).pack(
            side="left"
        )
        ttk.Button(acciones, text="Guardar parametros", command=self.guardar).pack(
            side="left", padx=10
        )

        # El resultado se muestra como texto coloreado segun la severidad.
        resultado = ttk.LabelFrame(contenedor, text="Alertas del sistema",
                                   style="Panel.TLabelframe", padding=14)
        resultado.pack(fill="both", expand=True)
        self.alertas = tk.Text(
            resultado, height=7, wrap="word", state="disabled",
            font=("Segoe UI", 11), relief="flat", padx=10, pady=8,
        )
        self.alertas.pack(fill="both", expand=True)
        self.alertas.tag_configure("normal", foreground="#177245")
        self.alertas.tag_configure("advertencia", foreground="#a35b00")
        self.alertas.tag_configure("critico", foreground="#b42318")
        self.evaluar()

    def _crear_control(self, padre, texto, variable, minimo, maximo, unidad):
        # Crea una barra reutilizable con su etiqueta y valor numerico actual.
        fila = tk.Frame(padre, bg="#ffffff")
        fila.pack(fill="x", pady=5)
        ttk.Label(fila, text=texto, width=22, background="#ffffff").pack(side="left")
        valor = ttk.Label(fila, width=10, anchor="e", background="#ffffff")
        valor.pack(side="right")
        ttk.Scale(
            fila, from_=minimo, to=maximo, variable=variable,
            command=lambda _: self._actualizar_valor(valor, variable, unidad),
        ).pack(side="left", fill="x", expand=True, padx=12)
        self._actualizar_valor(valor, variable, unidad)

    def _actualizar_valor(self, etiqueta, variable, unidad):
        etiqueta.configure(text=f"{variable.get():.0f}{unidad}")
        if hasattr(self, "alertas"):
            self.evaluar()

    def _hechos_actuales(self):
        # Convierte los valores visuales en el diccionario esperado por las reglas.
        return {
            "cpu_uso": round(self.cpu_uso.get()),
            "memoria_libre": round(self.memoria_libre.get()),
            "ping_respuesta": round(self.ping_respuesta.get()),
            "temperatura": round(self.temperatura.get()),
            "ventilador_encendido": self.ventilador_encendido.get(),
        }

    def evaluar(self):
        # Ejecuta el motor y reemplaza las alertas mostradas en la ventana.
        diagnosticos = diagnosticar_servidor(self._hechos_actuales())
        self.alertas.configure(state="normal")
        self.alertas.delete("1.0", "end")
        for diagnostico in diagnosticos:
            nivel = "critico" if diagnostico.startswith("CRITICO") else "advertencia"
            if diagnostico.startswith("NORMAL"):
                nivel = "normal"
            self.alertas.insert("end", f"- {diagnostico}\n\n", nivel)
        self.alertas.configure(state="disabled")

    def guardar(self):
        # Persiste los valores modificados para reutilizarlos en la proxima ejecucion.
        with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
            json.dump(self._hechos_actuales(), archivo, indent=4)
        messagebox.showinfo("Guardado", "Los parametros se guardaron correctamente.")


# 3. EJECUCIÓN
if __name__ == "__main__":
    raiz = tk.Tk()
    VentanaDiagnostico(raiz)
    raiz.mainloop()
