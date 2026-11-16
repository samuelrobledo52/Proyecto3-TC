from src.cinta import Cinta, mostrar


class MaquinaTuring:
    def __init__(self, estados, inicial, finales, alfabeto, alfabeto_cinta, delta, limite=10000):
        self.estados = estados
        self.inicial = inicial
        self.finales = finales
        self.alfabeto = alfabeto
        self.alfabeto_cinta = alfabeto_cinta
        self.delta = delta
        self.limite = limite
        self.reiniciar("")

    def reiniciar(self, cadena):
        self.cinta = Cinta(cadena)
        self.estado = self.inicial
        self.cache = None
        self.pasos = 0

    def descripcion(self):
        izquierda, derecha = self.cinta.partes()
        return f"{izquierda}[{self.estado}, {mostrar(self.cache)}]{derecha}"

    def paso(self):
        clave = (self.estado, self.cache, self.cinta.leer())
        if clave not in self.delta:
            return False
        estado, cache, escribir, movimiento = self.delta[clave]
        self.cinta.escribir(escribir)
        self.cinta.mover(movimiento)
        self.estado = estado
        self.cache = cache
        self.pasos += 1
        return True

    def simular(self, cadena):
        self.reiniciar(cadena)
        ids = [self.descripcion()]
        invalidos = [simbolo for simbolo in cadena if simbolo not in self.alfabeto_cinta]
        if invalidos:
            return ids, self.resultado(False, f"el símbolo '{invalidos[0]}' no pertenece al alfabeto de cinta")
        while self.pasos < self.limite:
            if not self.paso():
                if self.estado in self.finales:
                    return ids, self.resultado(True, f"se detuvo en el estado final {self.estado}")
                leido = mostrar(self.cinta.leer())
                return ids, self.resultado(False, f"no hay transición para ([{self.estado}, {mostrar(self.cache)}], {leido}) y {self.estado} no es final")
            ids.append(self.descripcion())
        return ids, self.resultado(False, f"se alcanzó el límite de {self.limite} pasos")

    def resultado(self, aceptada, motivo):
        return {
            "aceptada": aceptada,
            "motivo": motivo,
            "pasos": self.pasos,
            "cinta": self.cinta.visible(),
        }
