def resolver_lineal(a, b, c,):
    pasos = []

    #paso 1: ecuacion original
    

    if a == 0:
     pasos.append(f"{a}x + {b} = {c}")
     pasos.append("Como 0x = 0, la ecuación se reduce a:")
     pasos.append(f"{b} = {c}")

    if b == c:
        pasos.append("Ambos lados son iguales, por lo tanto hay infinitas soluciones.")
    else:
        pasos.append("Los valores no son iguales, por lo tanto no tiene solución.")

    return pasos
    

    #paso 2: restar b a ambos lados
    pasos.append(f"restamos {b} de ambos lados")
    nuevo_c = c - b
    pasos.append(f"{a}x = {nuevo_c}")

    #paso 3: dividir ambos lados entre a
    pasos.append(f"dividimos ambos lados entre {a}")    
    x = nuevo_c / a
    pasos.append(f"x = {x}")

    return pasos

# Ejemplo de uso
a = 0
b = 3
c = 5
pasos = resolver_lineal(a, b, c)
for paso in pasos:    print(paso)   


