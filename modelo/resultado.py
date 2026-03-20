from dataclasses import dataclass

from .partido import Partido


@dataclass(slots=True)
class ResultadoPartidoCircunscripcion:
    partido: Partido
    votos: int
    diputados_oficiales: int
    diputados_calculados: int = 0

    @property
    def votos_por_escano_oficial(self) -> float | None:
        if self.diputados_oficiales <= 0:
            return None
        return self.votos / self.diputados_oficiales

    @property
    def votos_por_escano_calculado(self) -> float | None:
        if self.diputados_calculados <= 0:
            return None
        return self.votos / self.diputados_calculados
