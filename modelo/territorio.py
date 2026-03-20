from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field

from .partido import Partido
from .resultado import ResultadoPartidoCircunscripcion


@dataclass(slots=True)
class Territorio(ABC):
    nombre: str
    codigo: str
    poblacion: int = 0
    numero_mesas: int = 0
    censo_sin_cera: int = 0
    censo_cera: int = 0
    censo_total: int = 0
    votantes_cer: int = 0
    votantes_cera: int = 0
    votantes_totales: int = 0
    votos_validos: int = 0
    votos_candidaturas: int = 0
    votos_blanco: int = 0
    votos_nulos: int = 0
    resultados: dict[str, ResultadoPartidoCircunscripcion] = field(default_factory=dict)

    def agregar_resultado(self, resultado: ResultadoPartidoCircunscripcion) -> None:
        self.resultados[resultado.partido.siglas] = resultado

    def resultado_de(self, partido: Partido) -> ResultadoPartidoCircunscripcion | None:
        return self.resultados.get(partido.siglas)

    @property
    def porcentaje_votos_nulos(self) -> float:
        if self.votantes_totales == 0:
            return 0.0
        return self.votos_nulos * 100 / self.votantes_totales

    @property
    def porcentaje_votos_blanco(self) -> float:
        if self.votos_validos == 0:
            return 0.0
        return self.votos_blanco * 100 / self.votos_validos

    @property
    def participacion_cera(self) -> float:
        if self.censo_cera == 0:
            return 0.0
        return self.votantes_cera * 100 / self.censo_cera

    @property
    def proporcion_cera_sobre_poblacion(self) -> float:
        if self.poblacion == 0:
            return 0.0
        return self.votantes_cera * 100 / self.poblacion

    def total_diputados_oficiales(self) -> int:
        total = 0
        for resultado in self.resultados.values():
            total += resultado.diputados_oficiales
        return total

    def total_diputados_calculados(self) -> int:
        total = 0
        for resultado in self.resultados.values():
            total += resultado.diputados_calculados
        return total


@dataclass(slots=True)
class Circunscripcion(Territorio):
    comunidad_nombre: str = ""


@dataclass(slots=True)
class ComunidadAutonoma(Territorio):
    circunscripciones: list[Circunscripcion] = field(default_factory=list)

    def agregar_circunscripcion(self, circunscripcion: Circunscripcion) -> None:
        self.circunscripciones.append(circunscripcion)


@dataclass(slots=True)
class Nacion(Territorio):
    comunidades: list[ComunidadAutonoma] = field(default_factory=list)

    def agregar_comunidad(self, comunidad: ComunidadAutonoma) -> None:
        self.comunidades.append(comunidad)
