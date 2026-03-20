from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from modelo.eleccion import EleccionCongreso2023
from modelo.partido import Partido
from modelo.resultado import ResultadoPartidoCircunscripcion
from modelo.territorio import Circunscripcion
from util.xlsx_reader import SimpleXlsxReader


@dataclass(slots=True)
class BloquePartidoExcel:
    indice_votos: int
    indice_diputados: int
    nombre: str
    siglas: str


class LectorExcelElecciones:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def cargar(self) -> EleccionCongreso2023:
        workbook = SimpleXlsxReader(self.file_path).read_sheets()
        hoja = None
        for candidate in workbook:
            if candidate.name == "Circunscripciones":
                hoja = candidate
                break
        if hoja is None:
            raise ValueError("No se ha encontrado la hoja 'Circunscripciones' en el Excel real.")
        filas = hoja.rows
        if len(filas) < 7:
            raise ValueError("El Excel no tiene suficientes filas para construir el modelo.")

        indice_encabezados = self._buscar_fila_encabezados(filas)
        fila_nombres_partido = filas[indice_encabezados - 2]
        fila_siglas_partido = filas[indice_encabezados - 1]
        fila_encabezados = filas[indice_encabezados]

        eleccion = EleccionCongreso2023()
        eleccion.hoja_origen = hoja.name
        eleccion.mapeo_excel = self._mapear_columnas_generales(fila_encabezados)

        bloques = self._detectar_bloques_partido(fila_nombres_partido, fila_siglas_partido, fila_encabezados)
        for bloque in bloques:
            eleccion.registrar_partido(Partido(nombre=bloque.nombre, siglas=bloque.siglas))

        for fila in filas[indice_encabezados + 1:]:
            if not any(valor != "" for valor in fila):
                continue
            circunscripcion = self._construir_circunscripcion(fila)
            if not circunscripcion.codigo or not circunscripcion.nombre:
                continue
            for bloque in bloques:
                votos = self._parse_int(self._safe_get(fila, bloque.indice_votos))
                diputados = self._parse_int(self._safe_get(fila, bloque.indice_diputados))
                if votos == 0:
                    continue
                resultado = ResultadoPartidoCircunscripcion(
                    partido=eleccion.partidos[bloque.siglas],
                    votos=votos,
                    diputados_oficiales=diputados,
                )
                circunscripcion.agregar_resultado(resultado)
            eleccion.registrar_circunscripcion(circunscripcion)
        return eleccion


    def _buscar_fila_encabezados(self, filas: list[list[str]]) -> int:
        for indice, fila in enumerate(filas):
            if len(fila) >= 15 and fila[:15] == [
                "Nombre de Comunidad",
                "Código de Provincia",
                "Nombre de Provincia",
                "Población",
                "Número de mesas",
                "Censo electoral sin CERA",
                "Censo CERA",
                "Total censo electoral",
                "Total votantes CER",
                "Total votantes CERA",
                "Total votantes",
                "Votos válidos",
                "Votos a candidaturas",
                "Votos en blanco",
                "Votos nulos",
            ]:
                return indice
        raise ValueError("No se ha localizado la fila real de encabezados en la hoja Circunscripciones.")

    def _mapear_columnas_generales(self, encabezados: list[str]) -> dict[str, str]:
        mapping = {
            "Nombre de Comunidad": "comunidad_nombre",
            "Código de Provincia": "codigo_provincia",
            "Nombre de Provincia": "nombre_provincia",
            "Población": "poblacion",
            "Número de mesas": "numero_mesas",
            "Censo electoral sin CERA": "censo_sin_cera",
            "Censo CERA": "censo_cera",
            "Total censo electoral": "censo_total",
            "Total votantes CER": "votantes_cer",
            "Total votantes CERA": "votantes_cera",
            "Total votantes": "votantes_totales",
            "Votos válidos": "votos_validos",
            "Votos a candidaturas": "votos_candidaturas",
            "Votos en blanco": "votos_blanco",
            "Votos nulos": "votos_nulos",
        }
        result = {}
        for encabezado in encabezados[:15]:
            if encabezado in mapping:
                result[encabezado] = mapping[encabezado]
        return result

    def _detectar_bloques_partido(
        self,
        fila_nombres_partido: list[str],
        fila_siglas_partido: list[str],
        fila_encabezados: list[str],
    ) -> list[BloquePartidoExcel]:
        bloques: list[BloquePartidoExcel] = []
        index = 15
        while index + 1 < len(fila_encabezados):
            if fila_encabezados[index] != "Votos":
                index += 1
                continue
            if fila_encabezados[index + 1] != "Diputados":
                raise ValueError("Se esperaba una columna 'Diputados' después de 'Votos'.")
            nombre = self._safe_get(fila_nombres_partido, index).strip()
            siglas = self._safe_get(fila_siglas_partido, index).strip()
            if nombre or siglas:
                bloques.append(
                    BloquePartidoExcel(
                        indice_votos=index,
                        indice_diputados=index + 1,
                        nombre=nombre,
                        siglas=siglas or nombre,
                    )
                )
            index += 2
        return bloques

    def _construir_circunscripcion(self, fila: list[str]) -> Circunscripcion:
        return Circunscripcion(
            nombre=self._safe_get(fila, 2),
            codigo=self._safe_get(fila, 1),
            comunidad_nombre=self._safe_get(fila, 0),
            poblacion=self._parse_int(self._safe_get(fila, 3)),
            numero_mesas=self._parse_int(self._safe_get(fila, 4)),
            censo_sin_cera=self._parse_int(self._safe_get(fila, 5)),
            censo_cera=self._parse_int(self._safe_get(fila, 6)),
            censo_total=self._parse_int(self._safe_get(fila, 7)),
            votantes_cer=self._parse_int(self._safe_get(fila, 8)),
            votantes_cera=self._parse_int(self._safe_get(fila, 9)),
            votantes_totales=self._parse_int(self._safe_get(fila, 10)),
            votos_validos=self._parse_int(self._safe_get(fila, 11)),
            votos_candidaturas=self._parse_int(self._safe_get(fila, 12)),
            votos_blanco=self._parse_int(self._safe_get(fila, 13)),
            votos_nulos=self._parse_int(self._safe_get(fila, 14)),
        )

    def _safe_get(self, fila: list[str], index: int) -> str:
        if index < len(fila):
            return fila[index]
        return ""

    def _parse_int(self, value: str) -> int:
        if value == "":
            return 0
        return int(float(value))
