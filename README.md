# Congreso 2023 · Analizador OO de elecciones generales

Aplicación académica en Python para estudiar los resultados de las elecciones generales españolas de 2023 al Congreso de los Diputados a partir del fichero `data/PROV_02_202307_1.xlsx`.

## Objetivo

El proyecto implementa una solución orientada a objetos, mantenible y defendible, separando:

- **modelo de dominio**;
- **servicios de lectura, agregación, validación y análisis**;
- **generación de gráficos**;
- **interfaz de escritorio con CustomTkinter**.

La circunscripción es la unidad base de lectura, cálculo y persistencia en memoria. Las comunidades autónomas y la nación se construyen exclusivamente por agregación de circunscripciones.

## Fuente de datos

La única fuente de entrada es:

- `data/PROV_02_202307_1.xlsx`

El lector no inventa columnas: inspecciona la hoja real `Circunscripciones` y mapea los encabezados presentes en el Excel.

## Estructura del proyecto

```text
.
├── data/
│   └── PROV_02_202307_1.xlsx
├── docs/
│   ├── dependencias.md
│   └── mapeo_excel.md
├── modelo/
│   ├── __init__.py
│   ├── eleccion.py
│   ├── estadisticas.py
│   ├── partido.py
│   ├── resultado.py
│   └── territorio.py
├── servicios/
│   ├── __init__.py
│   ├── agregador.py
│   ├── analizador.py
│   ├── dhondt.py
│   ├── graficos.py
│   ├── lector_excel.py
│   ├── pactometro.py
│   └── validador.py
├── tests/
│   └── test_elecciones.py
├── ui/
│   ├── __init__.py
│   ├── app.py
│   └── temas.py
├── util/
│   ├── __init__.py
│   └── xlsx_reader.py
├── main.py
└── requirements.txt
```

## Requisitos previos

- Python 3.11 o superior.
- Entorno virtual recomendado.
- El fichero Excel original del repositorio en `data/PROV_02_202307_1.xlsx`.

## Instalación

1. Crear entorno virtual:

   ```bash
   python -m venv .venv
   ```

2. Activarlo.

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

### Consola

```bash
python main.py --modo consola
```

### Interfaz gráfica

```bash
python main.py --modo ui
```

Si el modo UI no arranca, revisa antes:

1. que has instalado `pip install -r requirements.txt`;
2. que estás en una sesión gráfica real;
3. que en Linux existe `DISPLAY` o `WAYLAND_DISPLAY`.

El arranque valida dependencias y entorno gráfico para evitar trazas poco claras.

## Arquitectura resumida

- `modelo/`: entidades del dominio y agregados principales.
- `servicios/lector_excel.py`: lectura del Excel real y construcción del modelo OO.
- `servicios/agregador.py`: creación de CCAA y nación desde circunscripciones.
- `servicios/dhondt.py`: reparto de escaños con umbral del 3 % de votos válidos.
- `servicios/validador.py`: comprobaciones de coherencia del dataset y del modelo.
- `servicios/analizador.py`: consultas analíticas y rankings.
- `servicios/graficos.py`: generación de gráficos integrables en la UI.
- `servicios/pactometro.py`: combinaciones de partidos que alcanzan un umbral.
- `ui/`: dashboard en CustomTkinter con modo claro y oscuro completos.

## Flujo de datos

1. Se inspecciona la hoja `Circunscripciones` del Excel.
2. Se construye un mapeo explícito entre columnas reales y atributos del modelo.
3. Se crean partidos y circunscripciones.
4. Se omiten combinaciones partido-circunscripción con 0 votos.
5. Se agregan resultados autonómicos y nacionales.
6. Se recalculan escaños por D’Hondt con umbral del 3 %.
7. Se validan las coincidencias con los escaños oficiales.
8. La UI consume servicios ya calculados, sin recalcular negocio por su cuenta.

## Mapeo Excel

El mapeo detallado está documentado en `docs/mapeo_excel.md`.

## Interfaz

La aplicación incluye:

- sidebar lateral;
- top bar;
- selector de tema claro/oscuro;
- dashboard con KPIs;
- vistas de territorios, resultados, D’Hondt, análisis, gráficos, pactómetro y validación.

La UI está diseñada como dashboard analítico y reutiliza una paleta coherente en ambos temas.

## Tema claro y oscuro

Se implementan dos paletas completas:

- **oscuro**: fondos profundos, tarjetas diferenciadas y alto contraste;
- **claro**: paneles blancos, bordes suaves y textos oscuros legibles.

El cambio afecta paneles, tarjetas, badges, tablas y gráficos.

## Regla D’Hondt aplicada

En cada circunscripción se sigue este proceso:

1. calcular votos válidos;
2. excluir candidaturas por debajo del 3 %;
3. generar cocientes D’Hondt;
4. adjudicar escaños;
5. comparar el resultado calculado con el dato oficial del Excel.

## Funcionalidades implementadas

- lectura del Excel sin pandas;
- mapeo real de columnas;
- construcción OO del modelo electoral;
- agregación territorial;
- validación de coherencia;
- reparto D’Hondt;
- análisis estadístico;
- pactómetro;
- gráficos reutilizables;
- UI base en CustomTkinter.

## Limitaciones conocidas

- Las tablas avanzadas de la UI se implementan con widgets estándar de Tkinter/CustomTkinter; no hay grid virtualizado.
- La exportación de gráficos se deja encapsulada en el servicio y puede ampliarse.
- Algunas consultas complejas se muestran en modo resumen dentro de la UI para mantener claridad académica.

## Mejoras futuras

- persistencia de preferencias de usuario;
- filtros avanzados por partido y territorio en todas las vistas;
- exportación de informes a PDF;
- caché de gráficos renderizados.

## Dependencias

- Instalación: `requirements.txt`.
- Explicación técnica: `docs/dependencias.md`.

## Autoría

Proyecto preparado como base académica defendible para Programación Orientada a Objetos en Python.
