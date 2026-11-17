# Proyecto 3 - Simulador de Máquinas de Turing

Teoría de la Computación - Universidad del Valle de Guatemala

## Integrantes

- Samuel Robledo - 241282

## Requisitos e instalación

- Python 3.10 o superior
- PyYAML

```
python -m venv venv
venv\Scripts\activate        (Windows)
source venv/bin/activate     (Linux o macOS)
pip install -r requirements.txt
```

## Ejecución

```
python main.py maquinas/reconocedora.yaml
python main.py maquinas/alteradora.yaml
python main.py maquinas/ejemplo_enunciado.yaml
```

El programa simula todas las cadenas de `simulation_strings`, imprime las descripciones instantáneas y el resultado de cada una, y guarda la misma salida en `salidas/<nombre>.txt`.

Para correr las pruebas:

```
python pruebas/verificar.py
```

## Arquitectura

- `main.py`: recibe la ruta del YAML, ejecuta las simulaciones y escribe la salida en consola y en `salidas/`.
- `src/parser.py`: lee el YAML y valida claves faltantes, estados inicial y finales dentro de `q_list`, que `alphabet` esté contenido en `tape_alphabet`, que los estados y símbolos de cada transición existan, que el desplazamiento sea `L`, `R` o `S`, y que no haya dos transiciones para el mismo (estado, caché, símbolo). Si encuentra un error muestra un mensaje corto y termina.
- `src/cinta.py`: clase `Cinta`. La cinta es un diccionario `posición -> símbolo`, por lo que es infinita en ambos sentidos. Una celda que no está en el diccionario es blanco. Guarda la posición del cabezal y devuelve la porción visible sin blancos sobrantes.
- `src/maquina.py`: clase `MaquinaTuring` con los métodos `paso()` y `simular(cadena)`.

El estado de la máquina es el par `[q, c]`, donde `q` es el estado de control y `c` el valor de la caché. La delta se guarda en un diccionario con clave `(estado, caché, símbolo)` y valor `(nuevo estado, nueva caché, símbolo a escribir, movimiento)`. Un valor vacío o `null` en `mem_cache_value`, `tape_input` o `tape_output` se interpreta como blanco. Por ejemplo, δ([q0, B], a) = ([q1, a], B, R) lee `a` con la caché vacía, pasa a `q1` guardando `a` en la caché, escribe blanco y se mueve a la derecha.

Las descripciones instantáneas tienen la forma `α[q, c]β`, con el estado justo antes del símbolo que lee el cabezal. El blanco y la caché vacía se muestran como `B`. Cada ID se numera y se une a la anterior con `⊢`.

La simulación se detiene cuando no hay transición aplicable. La cadena se acepta si el estado actual es final y se rechaza en caso contrario. También se rechaza si la cadena contiene símbolos fuera de `tape_alphabet` o si se llega al límite de 10000 pasos.

## Máquina 1: reconocedora

Archivo: `maquinas/reconocedora.yaml`

Lenguaje: L = { aⁿbⁿcⁿ | n ≥ 1 }. Este lenguaje no es libre de contexto.

Definición formal: M = (Q, Σ, Γ, δ, q0, B, F)

- Q = {0, 1, 2, 3, 4, 5, 6} × {B} (esta máquina no usa la caché)
- Σ = {a, b, c}
- Γ = {a, b, c, X, Y, Z, B}
- q0 = [0, B]
- B = blanco
- F = {[6, B]}

| Estado | Caché | Lee | Nuevo estado | Nueva caché | Escribe | Mov. |
|---|---|---|---|---|---|---|
| 0 | `B` | `a` | 1 | `B` | `X` | R |
| 0 | `B` | `Y` | 4 | `B` | `Y` | R |
| 1 | `B` | `a` | 1 | `B` | `a` | R |
| 1 | `B` | `Y` | 1 | `B` | `Y` | R |
| 1 | `B` | `b` | 2 | `B` | `Y` | R |
| 2 | `B` | `b` | 2 | `B` | `b` | R |
| 2 | `B` | `Z` | 2 | `B` | `Z` | R |
| 2 | `B` | `c` | 3 | `B` | `Z` | L |
| 3 | `B` | `a` | 3 | `B` | `a` | L |
| 3 | `B` | `b` | 3 | `B` | `b` | L |
| 3 | `B` | `Y` | 3 | `B` | `Y` | L |
| 3 | `B` | `Z` | 3 | `B` | `Z` | L |
| 3 | `B` | `X` | 0 | `B` | `X` | R |
| 4 | `B` | `Y` | 4 | `B` | `Y` | R |
| 4 | `B` | `Z` | 5 | `B` | `Z` | R |
| 5 | `B` | `Z` | 5 | `B` | `Z` | R |
| 5 | `B` | `B` | 6 | `B` | `B` | S |

Algoritmo: en cada vuelta marca la primera `a` como `X`, avanza hasta la primera `b` y la marca como `Y`, avanza hasta la primera `c` y la marca como `Z`. Luego regresa a la `X` más a la izquierda y repite. Cuando ya no quedan `a`, el estado 4 y el 5 verifican que el resto de la cinta sea solo `Y` seguido de `Z` hasta el blanco, y entonces acepta. Cualquier símbolo fuera de lugar deja a la máquina sin transición y la cadena se rechaza.

| Cadena | Resultado esperado | Cinta final |
|---|---|---|
| aabbcc | ACEPTADA | XXYYZZ |
| aaabbbccc | ACEPTADA | XXXYYYZZZ |
| aabbbcc | RECHAZADA | XXYYbZZ |
| abcabc | RECHAZADA | XYZabc |

## Máquina 2: alteradora

Archivo: `maquinas/alteradora.yaml`

Función: f(w) = w#w, con w ∈ {a, b}⁺.

Definición formal: M = (Q, Σ, Γ, δ, q0, B, F)

- Q = {0, 1, 2, 3, 4, 5} × {a, b, B}
- Σ = {a, b}
- Γ = {a, b, X, Y, #, B}
- q0 = [0, B]
- B = blanco
- F = {[5, B]}

| Estado | Caché | Lee | Nuevo estado | Nueva caché | Escribe | Mov. |
|---|---|---|---|---|---|---|
| 0 | `B` | `a` | 0 | `B` | `a` | R |
| 0 | `B` | `b` | 0 | `B` | `b` | R |
| 0 | `B` | `B` | 1 | `B` | `#` | L |
| 1 | `B` | `a` | 1 | `B` | `a` | L |
| 1 | `B` | `b` | 1 | `B` | `b` | L |
| 1 | `B` | `B` | 2 | `B` | `B` | R |
| 2 | `B` | `a` | 3 | `a` | `X` | R |
| 2 | `B` | `b` | 3 | `b` | `Y` | R |
| 2 | `B` | `#` | 5 | `B` | `#` | S |
| 3 | `a` | `a` | 3 | `a` | `a` | R |
| 3 | `a` | `b` | 3 | `a` | `b` | R |
| 3 | `a` | `#` | 3 | `a` | `#` | R |
| 3 | `a` | `B` | 4 | `B` | `a` | L |
| 3 | `b` | `a` | 3 | `b` | `a` | R |
| 3 | `b` | `b` | 3 | `b` | `b` | R |
| 3 | `b` | `#` | 3 | `b` | `#` | R |
| 3 | `b` | `B` | 4 | `B` | `b` | L |
| 4 | `B` | `a` | 4 | `B` | `a` | L |
| 4 | `B` | `b` | 4 | `B` | `b` | L |
| 4 | `B` | `#` | 4 | `B` | `#` | L |
| 4 | `B` | `X` | 2 | `B` | `a` | R |
| 4 | `B` | `Y` | 2 | `B` | `b` | R |

Algoritmo: primero va al final de la cadena, escribe `#` y regresa al inicio. En el estado 2 marca el símbolo actual (`a` como `X`, `b` como `Y`) y lo guarda en la caché. En el estado 3 avanza hasta el primer blanco después del `#` y escribe el símbolo de la caché. En el estado 4 regresa hasta el marcador, lo restaura y avanza al siguiente símbolo. Cuando el estado 2 lee `#`, la copia está completa y pasa al estado final. Gracias a la caché basta un solo estado para transportar cualquiera de los dos símbolos.

| Cadena | Resultado esperado | Cinta final |
|---|---|---|
| abbab | ACEPTADA | abbab#abbab |
| aabba | ACEPTADA | aabba#aabba |
| babbb | ACEPTADA | babbb#babbb |
| bbaab | ACEPTADA | bbaab#bbaab |

## Máquina 3: ejemplo del enunciado

Archivo: `maquinas/ejemplo_enunciado.yaml`

Es el ejemplo incompleto del enunciado, con estados 0 a 5, Σ = {a, b}, Γ = {a, b, #, X, B} y solo dos transiciones. Se incluye para comprobar que el parser acepta el formato tal como aparece en el documento. Las tres cadenas se rechazan porque la máquina se queda sin transición antes de llegar al estado final.

| Estado | Caché | Lee | Nuevo estado | Nueva caché | Escribe | Mov. |
|---|---|---|---|---|---|---|
| 0 | `B` | `a` | 1 | `a` | `B` | R |
| 1 | `a` | `a` | 1 | `a` | `a` | R |

| Cadena | Resultado esperado |
|---|---|
| aab#aab | RECHAZADA |
| ab#ab | RECHAZADA |
| abbababa#aba | RECHAZADA |

## Pruebas

`pruebas/verificar.py` compara la reconocedora con una función de Python que decide aⁿbⁿcⁿ sobre todas las cadenas de {a, b, c} de longitud 1 a 9 (29523 cadenas), y la alteradora con `w + '#' + w` sobre todas las cadenas de {a, b} de longitud 1 a 7 (254 cadenas). También carga los archivos de `pruebas/errores/` y comprueba que cada uno produzca su mensaje de error.

## Video
https://youtu.be/8ScIJdCkxPc


[Enlace al video](PENDIENTE)

## Declaración de uso de IA

Se utilizó Claude para la corrección y revisión del trabajo; todo fue hecho, revisado y comprendido por mí.
