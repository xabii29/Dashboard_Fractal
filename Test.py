import funciones as fn

exit = False
graficas={
    1: "Sierpinski",
    2: "Arbol",
    3: "Cuadrados"
}

fn.limpiar_consola(0.5)
while exit == False:
    print("1.-Sierpinski\n2.-Arbol\n3.-Cuadrados\n\n")
    print("Selecciona la grafica a generar:\t")
    try:
        pasos = -1
        seleccion = int(input())
        fn.limpiar_consola()
        if seleccion not in graficas.keys():
            print("El numero seleccionado es erroneo\n")
            continue
        if seleccion == 1:
            fn.limpiar_consola()
            while pasos < 0 or pasos > 7:
                pasos = int(input("Cuantas veces se repite el fractal?:\t"))
                if pasos < 0 or pasos > 7:
                    print("Ingresa un valor positivo entero no mayor a 7")
                else:
                    fn.dibuja_sierpinski(pasos)
        if seleccion == 2:
            fn.limpiar_consola(0.5)
            while pasos < 0 or pasos > 15:
                pasos = int(input("Cuantas veces se repite el fractal?:\t"))
                if (pasos < 0) or (pasos > 15):
                    print("Ingresa un valor positivo entero no mayor a 15")
                else:
                    fn.dibuja_arbol(pasos)
        if seleccion == 3:
            fn.limpiar_consola(0.5)
            while pasos < 0 or pasos > 35:
                pasos = int(input("Cuantas veces se repite el fractal?:\t"))
                if (pasos < 0) or (pasos > 35):
                    print("Ingresa un valor positivo entero no mayor a 35")
                else:
                    fn.dibuja_cuadrados(pasos)
    except ValueError:
        fn.limpiar_consola()
        print("Ingresa un valor numerico que se encuentre en las opciones disponibles\n")
        continue
    
    salir = []
    while salir != "y":
        salir = input("Puedo generar mas imagenes, ¿Quieres salir? (Y/N):  ").lower()
        if salir != "y":
            if salir == "n":
                break
            fn.limpiar_consola()
            print("Elige una letra valida\n")
        else:
            exit = True

    fn.limpiar_consola()
    


