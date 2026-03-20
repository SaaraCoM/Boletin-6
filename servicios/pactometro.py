from __future__ import annotations

from itertools import combinations

from modelo.eleccion import EleccionCongreso2023


class Pactometro:
    def generar(self, eleccion: EleccionCongreso2023, umbral: int) -> list[tuple[list[str], int]]:
        if eleccion.nacion is None:
            return []
        partidos = []
        for resultado in eleccion.nacion.resultados.values():
            escanos = resultado.diputados_oficiales
            if escanos > 0:
                partidos.append((resultado.partido.siglas, escanos))
        soluciones = []
        for size in range(1, len(partidos) + 1):
            for combo in combinations(partidos, size):
                total = 0
                nombres = []
                for siglas, escanos in combo:
                    total += escanos
                    nombres.append(siglas)
                if total >= umbral:
                    soluciones.append((nombres, total))
        soluciones.sort(key=lambda item: (item[1], len(item[0])))
        return soluciones
