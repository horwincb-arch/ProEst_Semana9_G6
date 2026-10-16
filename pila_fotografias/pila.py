class Pila:
    """Administra una pila de fotografías mediante el principio LIFO."""

    def __init__(
        self,
        capacidad: int = 5,
        elementos: list[str] | None = None,
    ):
        """Inicializa la pila con una capacidad determinada."""

        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self.capacidad = capacidad
        self.elementos = list(elementos) if elementos is not None else []

        if len(self.elementos) > self.capacidad:
            raise ValueError(
                "La cantidad de fotografías supera la capacidad de la pila."
            )

    def esta_vacia(self) -> bool:
        """Comprueba si la pila está vacía."""

        return len(self.elementos) == 0

    def esta_llena(self) -> bool:
        """Comprueba si la pila alcanzó su capacidad máxima."""

        return len(self.elementos) >= self.capacidad

    def apilar(self, fotografia: str) -> None:
        """Agrega una fotografía al tope de la pila."""

        if self.esta_llena():
            raise OverflowError("La pila está llena.")

        if not isinstance(fotografia, str) or not fotografia.strip():
            raise ValueError("La referencia de la fotografía no es válida.")

        self.elementos.append(fotografia)

    def desapilar(self) -> str:
        """Retira y devuelve la fotografía situada en el tope."""

        if self.esta_vacia():
            raise IndexError("La pila está vacía.")

        return self.elementos.pop()

    def ver_tope(self) -> str | None:
        """Consulta la fotografía superior sin retirarla."""

        if self.esta_vacia():
            return None

        return self.elementos[-1]

    def limpiar(self) -> list[str]:
        """Vacía la pila y devuelve las fotografías retiradas."""

        fotografias = self.elementos.copy()
        self.elementos.clear()

        return fotografias

    def obtener_elementos(self) -> list[str]:
        """Devuelve una copia de las referencias almacenadas."""

        return self.elementos.copy()

    def cantidad(self) -> int:
        """Devuelve la cantidad de fotografías almacenadas."""

        return len(self.elementos)