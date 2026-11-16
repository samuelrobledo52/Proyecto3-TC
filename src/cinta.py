mostrar = lambda simbolo: "B" if simbolo is None else simbolo

MOVIMIENTOS = {"L": -1, "R": 1, "S": 0}


class Cinta:
    def __init__(self, cadena=""):
        self.celdas = {posicion: simbolo for posicion, simbolo in enumerate(cadena)}
        self.cabezal = 0

    def leer(self):
        return self.celdas.get(self.cabezal)

    def escribir(self, simbolo):
        if simbolo is None:
            self.celdas.pop(self.cabezal, None)
        else:
            self.celdas[self.cabezal] = simbolo

    def mover(self, direccion):
        self.cabezal += MOVIMIENTOS[direccion]

    def tramo(self, inicio, fin):
        return "".join(mostrar(self.celdas.get(posicion)) for posicion in range(inicio, fin))

    def visible(self):
        if not self.celdas:
            return "B"
        return self.tramo(min(self.celdas), max(self.celdas) + 1)

    def partes(self):
        inicio = min(min(self.celdas, default=self.cabezal), self.cabezal)
        fin = max(max(self.celdas, default=self.cabezal), self.cabezal)
        return self.tramo(inicio, self.cabezal), self.tramo(self.cabezal, fin + 1)
