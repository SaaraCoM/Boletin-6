from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from modelo.territorio import Territorio


class GeneradorGraficos:
    def grafico_barras_partidos(self, territorio: Territorio, metrica: str = "votos"):
        etiquetas = []
        valores = []
        for resultado in territorio.resultados.values():
            valor = resultado.votos if metrica == "votos" else resultado.diputados_oficiales
            if valor <= 0:
                continue
            etiquetas.append(resultado.partido.siglas)
            valores.append(valor)
        figura, eje = plt.subplots(figsize=(10, 5))
        eje.bar(etiquetas, valores, color="#4F46E5")
        eje.set_title(f"{metrica.title()} por partido · {territorio.nombre}")
        eje.tick_params(axis="x", rotation=45)
        figura.tight_layout()
        return figura

    def grafico_sectores_partidos(self, territorio: Territorio, metrica: str = "votos"):
        etiquetas = []
        valores = []
        for resultado in territorio.resultados.values():
            valor = resultado.votos if metrica == "votos" else resultado.diputados_oficiales
            if valor <= 0:
                continue
            etiquetas.append(resultado.partido.siglas)
            valores.append(valor)
        figura, eje = plt.subplots(figsize=(7, 7))
        eje.pie(valores, labels=etiquetas, autopct="%1.1f%%")
        eje.set_title(f"Distribución de {metrica} · {territorio.nombre}")
        figura.tight_layout()
        return figura

    def exportar(self, figura, destino: str | Path) -> None:
        figura.savefig(destino, dpi=150, bbox_inches="tight")
