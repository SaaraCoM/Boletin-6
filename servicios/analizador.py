from __future__ import annotations

from itertools import islice

from modelo.eleccion import EleccionCongreso2023
from modelo.partido import Partido
from modelo.territorio import Territorio
from servicios.dhondt import CalculadoraDhondt


class AnalizadorElectoral:
    def top_circunscripciones_nulos(self, eleccion: EleccionCongreso2023, n: int = 5) -> list[Territorio]:
        return sorted(eleccion.circunscripciones.values(), key=lambda item: item.porcentaje_votos_nulos, reverse=True)[:n]

    def top_ccaa_nulos(self, eleccion: EleccionCongreso2023, n: int = 5) -> list[Territorio]:
        return sorted(eleccion.comunidades.values(), key=lambda item: item.porcentaje_votos_nulos, reverse=True)[:n]

    def top_circunscripciones_blanco(self, eleccion: EleccionCongreso2023, n: int = 5) -> list[Territorio]:
        return sorted(eleccion.circunscripciones.values(), key=lambda item: item.porcentaje_votos_blanco, reverse=True)[:n]

    def top_ccaa_blanco(self, eleccion: EleccionCongreso2023, n: int = 5) -> list[Territorio]:
        return sorted(eleccion.comunidades.values(), key=lambda item: item.porcentaje_votos_blanco, reverse=True)[:n]

    def top_circunscripciones_cera(self, eleccion: EleccionCongreso2023, n: int = 5) -> list[Territorio]:
        return sorted(eleccion.circunscripciones.values(), key=lambda item: item.participacion_cera, reverse=True)[:n]

    def top_ccaa_cera(self, eleccion: EleccionCongreso2023, n: int = 5) -> list[Territorio]:
        return sorted(eleccion.comunidades.values(), key=lambda item: item.participacion_cera, reverse=True)[:n]

    def partidos_presentados_en_n_circunscripciones(self, eleccion: EleccionCongreso2023, n: int) -> list[Partido]:
        contador: dict[str, int] = {}
        for circunscripcion in eleccion.circunscripciones.values():
            for siglas in circunscripcion.resultados:
                contador[siglas] = contador.get(siglas, 0) + 1
        partidos = []
        for siglas, total in contador.items():
            if total == n:
                partidos.append(eleccion.partidos[siglas])
        return sorted(partidos, key=lambda partido: partido.siglas)

    def ccaa_con_mas_cera_proporcional(self, eleccion: EleccionCongreso2023, n: int = 5) -> list[Territorio]:
        return sorted(eleccion.comunidades.values(), key=lambda item: item.proporcion_cera_sobre_poblacion, reverse=True)[:n]

    def ultimo_escano_por_circunscripcion(self, eleccion: EleccionCongreso2023) -> list[dict[str, str | int]]:
        calculadora = CalculadoraDhondt()
        filas = []
        for circunscripcion in eleccion.circunscripciones.values():
            detalle = calculadora.calcular_para_circunscripcion(circunscripcion)
            filas.append({
                "circunscripcion": circunscripcion.nombre,
                "ultimo_escano": detalle.ultimo_escano_partido or "-",
                "se_quedo_cerca": detalle.siguiente_partido or "-",
                "votos_faltantes": detalle.votos_faltantes,
            })
        return filas

    def partido_con_mas_votos_sin_escano(self, eleccion: EleccionCongreso2023) -> tuple[str, str, int] | None:
        mejor = None
        for circunscripcion in eleccion.circunscripciones.values():
            for resultado in circunscripcion.resultados.values():
                if resultado.diputados_oficiales == 0:
                    candidate = (resultado.partido.siglas, circunscripcion.nombre, resultado.votos)
                    if mejor is None or candidate[2] > mejor[2]:
                        mejor = candidate
        return mejor

    def parejas_con_menos_votos_positivos(self, eleccion: EleccionCongreso2023, n: int) -> list[tuple[str, str, int]]:
        parejas = []
        for circunscripcion in eleccion.circunscripciones.values():
            for resultado in circunscripcion.resultados.values():
                parejas.append((resultado.partido.siglas, circunscripcion.nombre, resultado.votos))
        parejas.sort(key=lambda item: item[2])
        return list(islice(parejas, n))
