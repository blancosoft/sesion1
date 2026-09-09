# Sistema experto de diagnóstico de servidor

Aplicación de escritorio desarrollada en Python y Tkinter para evaluar el estado de un servidor mediante reglas de inferencia. Los parámetros iniciales se cargan desde `servidor_estado.json` y pueden modificarse desde la interfaz.

## Requisitos

- Windows
- Python 3
- Tkinter, incluido normalmente en la instalación estándar de Python

## Ejecución

Desde la carpeta del proyecto:

```powershell
python diagnostico_servidor.py
```

En Windows también se puede ejecutar `Ejecutar diagnostico.bat`.

## Funcionamiento

El sistema evalúa los siguientes parámetros:

- Uso de CPU
- Memoria libre
- Respuesta de ping
- Temperatura
- Estado del ventilador

Las reglas generan diagnósticos normales, advertencias o alertas críticas:

- Temperatura superior a 80 °C con el ventilador apagado: riesgo crítico de sobrecalentamiento.
- CPU superior al 90 % y memoria libre inferior al 10 %: posible caída inminente del servicio.
- Latencia superior a 500 ms: posible pérdida de conectividad.
- Valores elevados, pero no críticos: recomendación de revisar y monitorear el servidor.

Los parámetros modificados pueden guardarse con el botón **Guardar parámetros** para reutilizarlos en la siguiente ejecución.

## Archivos del proyecto

| Archivo | Descripción |
| --- | --- |
| `diagnostico_servidor.py` | Interfaz gráfica, base de reglas y motor de inferencia. |
| `servidor_estado.json` | Parámetros persistentes del servidor. |
| `Ejecutar diagnostico.bat` | Acceso directo de ejecución para Windows. |
| `LICENSE` | Licencia del proyecto. |

## Licencia

Consulta el archivo `LICENSE` incluido en este repositorio.