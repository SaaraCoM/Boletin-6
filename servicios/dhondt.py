from __future__ import annotations

from dataclasses import dataclass

from modelo.territorio import Circunscripcion


@dataclass(slots=True)
class DetalleDhondt:
    ultimo_escano_partido: str | None
    siguiente_partido: str | None
    votos_faltantes: int
    cocientes: list[tuple[str, float, int]]


class CalculadoraDhondt:
    def calcular_para_circunscripcion(self, circunscripcion: Circunscripcion) -> DetalleDhondt:
        escanos = circunscripcion.total_diputados_oficiales()
        if escanos <= 0:
            return DetalleDhondt(None, None, 0, [])
        umbral = circunscripcion.votos_validos * 0.03
        elegibles = []
        for resultado in circunscripcion.resultados.values():
            if resultado.votos >= umbral:
                elegibles.append(resultado)
            resultado.diputados_calculados = 0
        cocientes = []
        for resultado in elegibles:
            for divisor in range(1, escanos + 1):
                cocientes.append((resultado.partido.siglas, resultado.votos / divisor, divisor))
        cocientes.sort(key=lambda item: (-item[1], item[0]))
        top = cocientes[:escanos]
        for partido_siglas, _, _ in top:
            circunscripcion.resultados[partido_siglas].diputados_calculados += 1
        ultimo = top[-1] if top else None
        siguiente = cocientes[escanos] if len(cocientes) > escanos else None
        ultimo_partido = ultimo[0] if ultimo else None
        siguiente_partido = siguiente[0] if siguiente else None
        votos_faltantes = 0
        if ultimo and siguiente:
            divisor_siguiente = circunscripcion.resultados[siguiente_partido].diputados_calculados + 1
            objetivo = ultimo[1] * divisor_siguiente
            votos_faltantes = max(0, int(objetivo - circunscripcion.resultados[siguiente_partido].votos) + 1)
        return DetalleDhondt(ultimo_partido, siguiente_partido, votos_faltantes, top)
