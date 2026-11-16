import sys
from pathlib import Path

from src.parser import ErrorYAML, cargar


def formatear(ids):
    return [f"0: {ids[0]}"] + [f"⊢ {numero}: {descripcion}" for numero, descripcion in enumerate(ids[1:], start=1)]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.yaml>")
        sys.exit(1)
    ruta = Path(sys.argv[1])
    try:
        maquina, cadenas = cargar(ruta)
    except ErrorYAML as error:
        print(f"Error: {error}")
        sys.exit(1)

    lineas = [f"Máquina: {ruta.name}"]
    for cadena in cadenas:
        ids, resultado = maquina.simular(cadena)
        estado = "ACEPTADA" if resultado["aceptada"] else "RECHAZADA"
        lineas.append("")
        lineas.append(f"Cadena: {cadena if cadena else 'ε'}")
        lineas.extend(formatear(ids))
        lineas.append(f"Resultado: {estado} ({resultado['motivo']})")
        lineas.append(f"Pasos: {resultado['pasos']}")
        lineas.append(f"Cinta final: {resultado['cinta']}")

    texto = "\n".join(lineas)
    print(texto)
    carpeta = Path(__file__).resolve().parent / "salidas"
    carpeta.mkdir(exist_ok=True)
    (carpeta / f"{ruta.stem}.txt").write_text(texto + "\n", encoding="utf-8")
    print(f"\nSalida guardada en salidas/{ruta.stem}.txt")


if __name__ == "__main__":
    main()
