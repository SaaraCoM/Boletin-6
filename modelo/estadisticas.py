from dataclasses import dataclass

from .territorio import Territorio


@dataclass(slots=True)
class EstadisticasTerritoriales:
    territorio: Territorio

    def resumen(self) -> dict[str, float | int | str]:
        return {
            "territorio": self.territorio.nombre,
            "poblacion": self.territorio.poblacion,
            "censo_total": self.territorio.censo_total,
            "votantes_totales": self.territorio.votantes_totales,
            "votos_validos": self.territorio.votos_validos,
            "votos_blanco": self.territorio.votos_blanco,
            "votos_nulos": self.territorio.votos_nulos,
            "porcentaje_nulos": round(self.territorio.porcentaje_votos_nulos, 3),
            "porcentaje_blanco": round(self.territorio.porcentaje_votos_blanco, 3),
            "participacion_cera": round(self.territorio.participacion_cera, 3),
        }
