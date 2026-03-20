from __future__ import annotations

from dataclasses import dataclass

from modelo.eleccion import EleccionCongreso2023
from servicios.dhondt import CalculadoraDhondt


@dataclass(slots=True)
class IncidenciaValidacion:
    severidad: str
    territorio: str
    mensaje: str


class ValidadorCoherencia:
    def validar(self, eleccion: EleccionCongreso2023) -> list[IncidenciaValidacion]:
        incidencias: list[IncidenciaValidacion] = []
        incidencias.extend(self._validar_circunscripciones(eleccion))
        incidencias.extend(self._validar_agregaciones(eleccion))
        incidencias.extend(self._validar_dhondt(eleccion))
        return incidencias

    def _validar_circunscripciones(self, eleccion: EleccionCongreso2023) -> list[IncidenciaValidacion]:
        incidencias = []
        for circunscripcion in eleccion.circunscripciones.values():
            if circunscripcion.votos_candidaturas + circunscripcion.votos_blanco != circunscripcion.votos_validos:
                incidencias.append(IncidenciaValidacion(
                    "ERROR",
                    circunscripcion.nombre,
                    "Votos a candidaturas + votos en blanco no coincide con votos válidos.",
                ))
            if circunscripcion.votantes_totales != circunscripcion.votos_validos + circunscripcion.votos_nulos:
                incidencias.append(IncidenciaValidacion(
                    "ERROR",
                    circunscripcion.nombre,
                    "Votos válidos + nulos no coincide con total de votantes.",
                ))
        return incidencias

    def _validar_agregaciones(self, eleccion: EleccionCongreso2023) -> list[IncidenciaValidacion]:
        incidencias = []
        for comunidad in eleccion.comunidades.values():
            suma = 0
            for circunscripcion in comunidad.circunscripciones:
                suma += circunscripcion.votantes_totales
            if suma != comunidad.votantes_totales:
                incidencias.append(IncidenciaValidacion("ERROR", comunidad.nombre, "La agregación autonómica de votantes no cuadra."))
        if eleccion.nacion is not None:
            suma_nacional = 0
            for comunidad in eleccion.comunidades.values():
                suma_nacional += comunidad.votantes_totales
            if suma_nacional != eleccion.nacion.votantes_totales:
                incidencias.append(IncidenciaValidacion("ERROR", eleccion.nacion.nombre, "La agregación nacional de votantes no cuadra."))
        return incidencias

    def _validar_dhondt(self, eleccion: EleccionCongreso2023) -> list[IncidenciaValidacion]:
        incidencias = []
        calculadora = CalculadoraDhondt()
        for circunscripcion in eleccion.circunscripciones.values():
            calculadora.calcular_para_circunscripcion(circunscripcion)
            for resultado in circunscripcion.resultados.values():
                if resultado.diputados_calculados != resultado.diputados_oficiales:
                    incidencias.append(IncidenciaValidacion(
                        "AVISO",
                        circunscripcion.nombre,
                        f"{resultado.partido.siglas}: oficiales={resultado.diputados_oficiales}, calculados={resultado.diputados_calculados}",
                    ))
        return incidencias
