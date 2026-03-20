from __future__ import annotations

import argparse
import importlib
import os
import sys

from servicios.agregador import AgregadorTerritorial
from servicios.analizador import AnalizadorElectoral
from servicios.lector_excel import LectorExcelElecciones
from servicios.validador import ValidadorCoherencia


DEPENDENCIAS_UI = {
    "customtkinter": "Interfaz principal basada en CustomTkinter.",
    "matplotlib": "Renderizado de gráficos integrados en la interfaz.",
}


def construir_eleccion():
    lector = LectorExcelElecciones("data/PROV_02_202307_1.xlsx")
    eleccion = lector.cargar()
    return AgregadorTerritorial().agregar(eleccion)


def ejecutar_consola() -> None:
    eleccion = construir_eleccion()
    analizador = AnalizadorElectoral()
    incidencias = ValidadorCoherencia().validar(eleccion)
    print(f"Circunscripciones: {len(eleccion.circunscripciones)}")
    print(f"Comunidades: {len(eleccion.comunidades)}")
    if eleccion.nacion is not None:
        print(f"Escaños oficiales nacionales: {eleccion.nacion.total_diputados_oficiales()}")
    print(f"Incidencias de validación: {len(incidencias)}")
    mejor = analizador.partido_con_mas_votos_sin_escano(eleccion)
    if mejor is not None:
        print(f"Partido con más votos sin escaño: {mejor[0]} en {mejor[1]} con {mejor[2]} votos")


def validar_dependencias_ui() -> list[str]:
    faltantes = []
    for modulo in DEPENDENCIAS_UI:
        try:
            importlib.import_module(modulo)
        except ModuleNotFoundError:
            faltantes.append(modulo)
    return faltantes


def validar_entorno_grafico() -> bool:
    if sys.platform.startswith("win"):
        return True
    if sys.platform == "darwin":
        return True
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def ejecutar_ui() -> int:
    faltantes = validar_dependencias_ui()
    if faltantes:
        print("No se puede iniciar la interfaz porque faltan dependencias opcionales de UI.", file=sys.stderr)
        for modulo in faltantes:
            print(f"- {modulo}: {DEPENDENCIAS_UI[modulo]}", file=sys.stderr)
        print("Instala los paquetes con: pip install -r requirements.txt", file=sys.stderr)
        return 1

    if not validar_entorno_grafico():
        print("No se puede iniciar la interfaz porque no hay una sesión gráfica disponible.", file=sys.stderr)
        print("En Linux debes definir DISPLAY o abrir la aplicación desde un escritorio gráfico.", file=sys.stderr)
        return 1

    from ui.app import AplicacionElecciones

    eleccion = construir_eleccion()
    app = AplicacionElecciones(eleccion)
    app.mainloop()
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--modo", choices=["consola", "ui"], default="consola")
    args = parser.parse_args()
    if args.modo == "ui":
        raise SystemExit(ejecutar_ui())
    ejecutar_consola()
