from __future__ import annotations

import argparse

from servicios.agregador import AgregadorTerritorial
from servicios.analizador import AnalizadorElectoral
from servicios.lector_excel import LectorExcelElecciones
from servicios.validador import ValidadorCoherencia


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


def ejecutar_ui() -> None:
    from ui.app import AplicacionElecciones

    eleccion = construir_eleccion()
    app = AplicacionElecciones(eleccion)
    app.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--modo", choices=["consola", "ui"], default="consola")
    args = parser.parse_args()
    if args.modo == "ui":
        ejecutar_ui()
    else:
        ejecutar_consola()
