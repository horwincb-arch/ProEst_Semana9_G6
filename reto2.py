historial = []
pagina_actual = ""

while True:
    print("\n===== HISTORIAL DE NAVEGACION =====")
    print("1. Visitar pagina")
    print("2. Regresar")
    print("3. Mostrar pagina actual")
    print("4. Mostrar historial")
    print("0. Salir")

    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        pagina = input("Ingrese la pagina que desea visitar: ")

        if pagina_actual != "":
            historial.append(pagina_actual)

        pagina_actual = pagina
        print(f"Visitar: {pagina_actual}")

    elif opcion == "2":
        if len(historial) > 0:
            pagina_actual = historial.pop()
            print(f"Regresar -> {pagina_actual}")
        else:
            pagina_actual = ""
            print("Regresar -> sin anterior")

    elif opcion == "3":
        if pagina_actual != "":
            print(f"Pagina actual: {pagina_actual}")
        else:
            print("No hay ninguna pagina abierta.")
    elif opcion == "4":
        print("Historial:", historial)
    elif opcion == "0":
        print("Programa finalizado.")
        break
    else:
        print("Opcion invalida.")