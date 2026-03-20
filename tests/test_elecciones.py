from servicios.agregador import AgregadorTerritorial
from servicios.analizador import AnalizadorElectoral
from servicios.dhondt import CalculadoraDhondt
from servicios.lector_excel import LectorExcelElecciones
from servicios.pactometro import Pactometro
from servicios.validador import ValidadorCoherencia


DATASET = "data/PROV_02_202307_1.xlsx"


def construir_eleccion():
    eleccion = LectorExcelElecciones(DATASET).cargar()
    return AgregadorTerritorial().agregar(eleccion)


def test_carga_circunscripciones_y_partidos():
    eleccion = construir_eleccion()
    assert len(eleccion.circunscripciones) == 52
    assert len(eleccion.partidos) > 10
    assert "Nombre de Comunidad" in eleccion.mapeo_excel


def test_omision_de_resultados_con_cero_votos():
    eleccion = construir_eleccion()
    almeria = eleccion.circunscripciones["4"]
    assert "ERC" not in almeria.resultados
    assert "PP" in almeria.resultados


def test_agregacion_nacional_y_validacion_basica():
    eleccion = construir_eleccion()
    assert eleccion.nacion is not None
    assert eleccion.nacion.votantes_totales == sum(item.votantes_totales for item in eleccion.circunscripciones.values())
    incidencias = ValidadorCoherencia().validar(eleccion)
    assert isinstance(incidencias, list)


def test_dhondt_almeria():
    eleccion = construir_eleccion()
    detalle = CalculadoraDhondt().calcular_para_circunscripcion(eleccion.circunscripciones["4"])
    assert detalle.ultimo_escano_partido is not None
    assert eleccion.circunscripciones["4"].total_diputados_calculados() == eleccion.circunscripciones["4"].total_diputados_oficiales()


def test_analisis_y_pactometro():
    eleccion = construir_eleccion()
    analizador = AnalizadorElectoral()
    top = analizador.top_circunscripciones_nulos(eleccion, 3)
    assert len(top) == 3
    pactos = Pactometro().generar(eleccion, 176)
    assert pactos


def test_validacion_dependencias_ui_devuelve_lista():
    import main

    faltantes = main.validar_dependencias_ui()
    assert isinstance(faltantes, list)


def test_validacion_entorno_grafico_devuelve_bool():
    import main

    assert isinstance(main.validar_entorno_grafico(), bool)
