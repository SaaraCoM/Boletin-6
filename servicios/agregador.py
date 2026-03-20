from __future__ import annotations

from modelo.eleccion import EleccionCongreso2023
from modelo.resultado import ResultadoPartidoCircunscripcion
from modelo.territorio import ComunidadAutonoma, Nacion, Territorio


class AgregadorTerritorial:
    def agregar(self, eleccion: EleccionCongreso2023) -> EleccionCongreso2023:
        comunidades: dict[str, ComunidadAutonoma] = {}
        for circunscripcion in eleccion.circunscripciones.values():
            comunidad = comunidades.get(circunscripcion.comunidad_nombre)
            if comunidad is None:
                comunidad = ComunidadAutonoma(nombre=circunscripcion.comunidad_nombre, codigo=circunscripcion.comunidad_nombre)
                comunidades[comunidad.nombre] = comunidad
            comunidad.agregar_circunscripcion(circunscripcion)
            self._sumar_territorio(destino=comunidad, origen=circunscripcion)
        eleccion.comunidades = comunidades

        nacion = Nacion(nombre="España", codigo="ES")
        for comunidad in comunidades.values():
            nacion.agregar_comunidad(comunidad)
            self._sumar_territorio(destino=nacion, origen=comunidad)
        eleccion.nacion = nacion
        return eleccion

    def _sumar_territorio(self, destino: Territorio, origen: Territorio) -> None:
        destino.poblacion += origen.poblacion
        destino.numero_mesas += origen.numero_mesas
        destino.censo_sin_cera += origen.censo_sin_cera
        destino.censo_cera += origen.censo_cera
        destino.censo_total += origen.censo_total
        destino.votantes_cer += origen.votantes_cer
        destino.votantes_cera += origen.votantes_cera
        destino.votantes_totales += origen.votantes_totales
        destino.votos_validos += origen.votos_validos
        destino.votos_candidaturas += origen.votos_candidaturas
        destino.votos_blanco += origen.votos_blanco
        destino.votos_nulos += origen.votos_nulos
        for resultado in origen.resultados.values():
            existente = destino.resultados.get(resultado.partido.siglas)
            if existente is None:
                destino.resultados[resultado.partido.siglas] = ResultadoPartidoCircunscripcion(
                    partido=resultado.partido,
                    votos=resultado.votos,
                    diputados_oficiales=resultado.diputados_oficiales,
                    diputados_calculados=resultado.diputados_calculados,
                )
                continue
            existente.votos += resultado.votos
            existente.diputados_oficiales += resultado.diputados_oficiales
            existente.diputados_calculados += resultado.diputados_calculados
