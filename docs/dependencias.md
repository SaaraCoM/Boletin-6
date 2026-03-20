# Dependencias del proyecto

## Dependencias obligatorias

### customtkinter
- **Propósito**: interfaz de escritorio moderna sobre Tkinter.
- **Módulo que la usa**: `ui/`.
- **Obligatoria u opcional**: obligatoria para el modo visual.
- **Motivo de elección**: resuelve de forma simple el estilo moderno, el modo oscuro/claro y la construcción de dashboards sin introducir frameworks más complejos.

### matplotlib
- **Propósito**: generación de gráficos de barras y sectores.
- **Módulo que la usa**: `servicios/graficos.py` y la UI al incrustar figuras.
- **Obligatoria u opcional**: obligatoria si se quieren gráficos.
- **Motivo de elección**: biblioteca pública, estable y ampliamente documentada; suficiente para una aplicación académica sin dependencias pesadas adicionales.

### Pillow
- **Propósito**: soporte de imágenes cuando CustomTkinter lo requiere en algunos widgets y para futuras ampliaciones visuales.
- **Módulo que la usa**: `ui/`.
- **Obligatoria u opcional**: práctica y recomendada.
- **Motivo de elección**: dependencia ligera y habitual en interfaces Tk/CustomTkinter.

## Dependencias evitadas

### pandas
- **Razón para no usarla**: el enunciado lo prohíbe expresamente.
- **Alternativa aplicada**: lectura manual del formato XLSX mediante ZIP + XML con biblioteca estándar en `util/xlsx_reader.py`.

### openpyxl
- **Razón para no usarla**: no es estrictamente necesaria para este proyecto y se prioriza minimizar dependencias.
- **Alternativa aplicada**: parser propio enfocado al fichero real del repositorio.
