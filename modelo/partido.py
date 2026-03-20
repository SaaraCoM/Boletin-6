from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Partido:
    nombre: str
    siglas: str
    color: str = field(default="#4F46E5")

    def etiqueta(self) -> str:
        if self.siglas:
            return self.siglas
        return self.nombre
