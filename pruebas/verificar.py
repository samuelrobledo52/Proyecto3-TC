import sys
from itertools import product
from pathlib import Path

raiz = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(raiz))

from src.parser import ErrorYAML, cargar


def es_anbncn(cadena):
    n = len(cadena) // 3
    return n >= 1 and cadena == "a" * n + "b" * n + "c" * n


def cadenas(alfabeto, minimo, maximo):
    for longitud in range(minimo, maximo + 1):
        for letras in product(alfabeto, repeat=longitud):
            yield "".join(letras)


def probar_reconocedora():
    maquina, _ = cargar(raiz / "maquinas" / "reconocedora.yaml")
    total = 0
    fallos = []
    for cadena in cadenas("abc", 1, 9):
        total += 1
        _, resultado = maquina.simular(cadena)
        if resultado["aceptada"] != es_anbncn(cadena):
            fallos.append(cadena)
    return total, fallos


def probar_alteradora():
    maquina, _ = cargar(raiz / "maquinas" / "alteradora.yaml")
    total = 0
    fallos = []
    for cadena in cadenas("ab", 1, 7):
        total += 1
        _, resultado = maquina.simular(cadena)
        if not resultado["aceptada"] or resultado["cinta"] != cadena + "#" + cadena:
            fallos.append(cadena)
    return total, fallos


def probar_errores():
    fallos = []
    for ruta in sorted((raiz / "pruebas" / "errores").glob("*.yaml")):
        try:
            cargar(ruta)
            fallos.append(ruta.name)
            print(f"  {ruta.name}: no detectó el error")
        except ErrorYAML as error:
            print(f"  {ruta.name}: Error: {error}")
    return fallos


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    exito = True
    for nombre, prueba in (("Reconocedora", probar_reconocedora), ("Alteradora", probar_alteradora)):
        total, fallos = prueba()
        correctas = total - len(fallos)
        print(f"{nombre}: {correctas}/{total} coinciden ({correctas * 100 / total:.1f}%)")
        if fallos:
            exito = False
            print(f"  Fallos: {fallos[:10]}")
    print("YAML con errores:")
    if probar_errores():
        exito = False
    print("Resultado: todas las pruebas pasaron" if exito else "Resultado: hay pruebas fallidas")
    sys.exit(0 if exito else 1)


if __name__ == "__main__":
    main()
