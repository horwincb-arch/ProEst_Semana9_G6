pila = []
LIMITE = 5

while True:
    print("\n========== CONTROL DE BODEGA ==========")
    print("1. Apilar caja")
    print("2. Desapilar caja")
    print("3. Consultar tope")
    print("4. Mostrar pila")
    print("5. Salir")
    print("=======================================")

    opcion = input("Seleccione una opción: ").strip()
    if opcion == "1":
        if len(pila) >= LIMITE:
            print("La pila está llena. Máximo 5 cajas.")
        else:
            codigo = input("Ingrese el código de la caja: ").strip()

            if codigo == "":
                print("Error: el código no puede estar vacío.")
            elif codigo in pila:
                print("Error: ese código ya existe.")
            else:
                pila.append(codigo)
                print("Caja", codigo, "apilada correctamente.")

    elif opcion == "2":
        if len(pila) == 0:
            print("No se puede desapilar: la pila está vacía.")
        else:
            caja = pila.pop()
            print("Se retiró la caja:", caja)

    elif opcion == "3":
        if len(pila) == 0:
            print("La pila está vacía. No hay caja en el tope.")
        else:
            print("Caja en el tope:", pila[-1])

    elif opcion == "4":
        print("\n========== PILA DE CAJAS ==========")

        if len(pila) == 0:
            print("La pila está vacía.")
        else:
            for i in range(len(pila) - 1, -1, -1):
                print("+----------------------+")
                print("| Caja:", pila[i].ljust(10), "|")
                print("+----------------------+")

        print("Cantidad de cajas:", len(pila))
        print("Espacios disponibles:", LIMITE - len(pila))
        print("===================================")

    elif opcion == "5":
        print("Saliendo del sistema de bodega...")
        break

    else:
        print("Opción inválida. Seleccione del 1 al 5.")