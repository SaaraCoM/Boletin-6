# Mapeo explícito entre Excel real y modelo

## Hoja inspeccionada

- **Nombre real**: `Circunscripciones`

## Filas de encabezado reales

- **Fila 4**: nombre largo del partido.
- **Fila 5**: sigla del partido.
- **Fila 6**: nombres reales de columnas generales y bloques repetidos `Votos` / `Diputados`.

## Columnas generales

| Columna real | Atributo de modelo |
| --- | --- |
| Nombre de Comunidad | `comunidad_nombre` |
| Código de Provincia | `codigo_provincia` |
| Nombre de Provincia | `nombre_provincia` |
| Población | `poblacion` |
| Número de mesas | `numero_mesas` |
| Censo electoral sin CERA | `censo_sin_cera` |
| Censo CERA | `censo_cera` |
| Total censo electoral | `censo_total` |
| Total votantes CER | `votantes_cer` |
| Total votantes CERA | `votantes_cera` |
| Total votantes | `votantes_totales` |
| Votos válidos | `votos_validos` |
| Votos a candidaturas | `votos_candidaturas` |
| Votos en blanco | `votos_blanco` |
| Votos nulos | `votos_nulos` |

## Bloques de partidos

A partir de la columna `P`, el Excel alterna dos columnas por partido:

- `Votos`
- `Diputados`

El nombre real del partido se toma de la fila 4 y la sigla de la fila 5.

Ejemplo:

| Columnas reales | Partido detectado | Atributos |
| --- | --- | --- |
| P-Q | PARTIDO POPULAR / PP | `votos`, `diputados_oficiales` |
| R-S | PARTIDO SOCIALISTA OBRERO ESPAÑOL / PSOE | `votos`, `diputados_oficiales` |
| T-U | VOX / VOX | `votos`, `diputados_oficiales` |
| V-W | SUMAR / SUMAR | `votos`, `diputados_oficiales` |

## Regla de carga

Si un partido tiene `0` votos en una circunscripción, **no se crea** un objeto `ResultadoPartidoCircunscripcion` para esa combinación.
