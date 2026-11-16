import yaml

from src.cinta import MOVIMIENTOS, mostrar
from src.maquina import MaquinaTuring


class ErrorYAML(Exception):
    pass


def simbolo(valor):
    if valor is None:
        return None
    texto = str(valor)
    return texto if texto else None


def exigir(datos, claves, lugar):
    if not isinstance(datos, dict):
        raise ErrorYAML(f"{lugar} debe ser un diccionario")
    faltantes = [clave for clave in claves if clave not in datos]
    if faltantes:
        raise ErrorYAML(f"falta la clave '{faltantes[0]}' en {lugar}")


def lista(valor, nombre):
    if not isinstance(valor, list):
        raise ErrorYAML(f"'{nombre}' debe ser una lista")
    return valor


def leer_archivo(ruta):
    try:
        with open(ruta, encoding="utf-8") as archivo:
            return yaml.safe_load(archivo)
    except FileNotFoundError:
        raise ErrorYAML(f"no se encontró el archivo '{ruta}'")
    except yaml.YAMLError:
        raise ErrorYAML(f"el archivo '{ruta}' no es un YAML válido")


def cargar(ruta):
    datos = leer_archivo(ruta)
    exigir(datos, ["q_states", "alphabet", "tape_alphabet", "delta", "simulation_strings"], "el archivo")
    exigir(datos["q_states"], ["q_list", "initial", "final"], "q_states")

    estados = {str(estado) for estado in lista(datos["q_states"]["q_list"], "q_list")}
    inicial = str(datos["q_states"]["initial"])
    final = datos["q_states"]["final"]
    finales = {str(estado) for estado in (final if isinstance(final, list) else [final])}

    if inicial not in estados:
        raise ErrorYAML(f"el estado inicial '{inicial}' no está en q_list")
    for estado in finales:
        if estado not in estados:
            raise ErrorYAML(f"el estado final '{estado}' no está en q_list")

    alfabeto = {simbolo(valor) for valor in lista(datos["alphabet"], "alphabet")}
    alfabeto_cinta = {simbolo(valor) for valor in lista(datos["tape_alphabet"], "tape_alphabet")}
    alfabeto_cinta.add(None)
    if None in alfabeto:
        raise ErrorYAML("alphabet no puede contener el símbolo blanco")
    for valor in alfabeto:
        if valor not in alfabeto_cinta:
            raise ErrorYAML(f"el símbolo '{valor}' de alphabet no está en tape_alphabet")

    delta = {}
    for numero, transicion in enumerate(lista(datos["delta"], "delta"), start=1):
        lugar = f"la transición {numero}"
        exigir(transicion, ["params", "output"], lugar)
        entrada = transicion["params"]
        salida = transicion["output"]
        exigir(entrada, ["initial_state"], f"params de {lugar}")
        exigir(salida, ["final_state", "tape_displacement"], f"output de {lugar}")

        origen = str(entrada["initial_state"])
        destino = str(salida["final_state"])
        for estado in (origen, destino):
            if estado not in estados:
                raise ErrorYAML(f"el estado '{estado}' de {lugar} no está en q_list")

        cache = simbolo(entrada.get("mem_cache_value"))
        leido = simbolo(entrada.get("tape_input"))
        nueva_cache = simbolo(salida.get("mem_cache_value"))
        escrito = simbolo(salida.get("tape_output"))
        for valor in (cache, leido, nueva_cache, escrito):
            if valor not in alfabeto_cinta:
                raise ErrorYAML(f"el símbolo '{valor}' de {lugar} no está en tape_alphabet")

        movimiento = str(salida["tape_displacement"])
        if movimiento not in MOVIMIENTOS:
            raise ErrorYAML(f"desplazamiento '{movimiento}' inválido en {lugar}, debe ser L, R o S")

        clave = (origen, cache, leido)
        if clave in delta:
            raise ErrorYAML(f"transición duplicada para ([{origen}, {mostrar(cache)}], {mostrar(leido)}) en {lugar}")
        delta[clave] = (destino, nueva_cache, escrito, movimiento)

    cadenas = ["" if cadena is None else str(cadena) for cadena in lista(datos["simulation_strings"], "simulation_strings")]
    maquina = MaquinaTuring(estados, inicial, finales, alfabeto, alfabeto_cinta, delta)
    return maquina, cadenas
