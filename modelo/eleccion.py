from __future__ import annotations

from dataclasses import dataclass, field

from .partido import Partido
from .territorio import Circunscripcion, ComunidadAutonoma, Nacion


@dataclass(slots=True)
class EleccionCongreso2023:
    partidos: dict[str, Partido] = field(default_factory=dict)
    circunscripciones: dict[str, Circunscripcion] = field(default_factory=dict)
    comunidades: dict[str, ComunidadAutonoma] = field(default_factory=dict)
    nacion: Nacion | None = None
    mapeo_excel: dict[str, str] = field(default_factory=dict)
    hoja_origen: str = "Circunscripciones"

    def registrar_partido(self, partido: Partido) -> None:
        self.partidos[partido.siglas] = partido

    def registrar_circunscripcion(self, circunscripcion: Circunscripcion) -> None:
        self.circunscripciones[circunscripcion.codigo] = circunscripcion

    def registrar_comunidad(self, comunidad: ComunidadAutonoma) -> None:
        self.comunidades[comunidad.nombre] = comunidad

    def obtener_partidos_ordenados(self) -> list[Partido]:
        return sorted(self.partidos.values(), key=lambda partido: partido.siglas)
