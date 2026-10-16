class Pila:
    """Representa una pila de elementos que funciona con LIFO."""

    def __init__(self, capacidad: int, elementos: list[str] | None = None):
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self.capacidad = capacidad
        self.elementos = list(elementos) if elementos is not None else []

        if len(self.elementos) > self.capacidad:
            raise ValueError("Los elementos superan la capacidad de la pila.")

    def esta_vacia(self) -> bool:
        """Comprueba si la pila está vacía."""
        return len(self.elementos) == 0

    def esta_llena(self) -> bool:
        """Comprueba si la pila alcanzó su capacidad máxima."""
        return len(self.elementos) >= self.capacidad

    def apilar(self, elemento: str) -> None:
        """Agrega un elemento a la parte superior de la pila."""
        if self.esta_llena():
            raise OverflowError("La pila está llena.")

        if not isinstance(elemento, str) or not elemento.strip():
            raise ValueError("El elemento no puede estar vacío.")

        self.elementos.append(elemento.strip())

    def desapilar(self) -> str:
        """Retira y devuelve el elemento superior de la pila."""
        if self.esta_vacia():
            raise IndexError("La pila está vacía.")

        return self.elementos.pop()

    def ver_tope(self) -> str | None:
        """Devuelve el elemento superior sin retirarlo."""
        if self.esta_vacia():
            return None

        return self.elementos[-1]

    def limpiar(self) -> None:
        """Elimina todos los elementos de la pila."""
        self.elementos.clear()

    def obtener_elementos(self) -> list[str]:
        """Devuelve una copia de los elementos de la pila."""
        return self.elementos.copy()

    def cantidad(self) -> int:
        """Devuelve la cantidad actual de elementos."""
        return len(self.elementos)