from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# 🔧 separar términos
def separar_terminos(expresion):
    return re.findall(r'[+-]?\d*x|[+-]?\d+', expresion)

def resolver_ecuacion(ecuacion):
    pasos = []

    if "=" not in ecuacion:
        return ["Error: la ecuación debe tener '='"]

    if "x" not in ecuacion:
        return ["Error: la ecuación debe tener una variable 'x'"]

    try:
        ecuacion = ecuacion.replace(" ", "")
        pasos.append(f"Ecuación original: {ecuacion}")
        pasos.append("Queremos dejar la x completamente sola")

        izq, der = ecuacion.split("=")

        match = re.match(r'([+-]?\d*)x([+-]\d+)?', izq)

        if not match:
            return ["Error: formato no soportado (usa algo como 2x+3=7)"]

        coef = match.group(1)
        constante = match.group(2)

        # coeficiente de x
        if coef in ["", "+"]:
            a = 1
        elif coef == "-":
            a = -1
        else:
            a = int(coef)

        # constante
        b_izq = int(constante) if constante else 0
        b_der = int(der)

        # 🔹 PASO 1: eliminar constante
        if b_izq > 0:
            pasos.append(f"El {b_izq} está sumando, así que hacemos lo contrario")
            pasos.append(f"Restamos {b_izq} en ambos lados")
            nuevo_der = b_der - b_izq
        elif b_izq < 0:
            pasos.append(f"El {abs(b_izq)} está restando, así que hacemos lo contrario")
            pasos.append(f"Sumamos {abs(b_izq)} en ambos lados")
            nuevo_der = b_der + abs(b_izq)
        else:
            nuevo_der = b_der

        pasos.append(f"{a}x = {nuevo_der}")

        # 🔹 PASO 2: dividir
        if a != 1:
            pasos.append(f"El {a} está multiplicando a x")
            pasos.append("Hacemos la operación contraria")
            pasos.append(f"Dividimos ambos lados entre {a}")

        x = nuevo_der / a

        if x.is_integer():
            x = int(x)

        pasos.append(f"x = {x}")
        pasos.append("Listo, hemos encontrado el valor de x 🎉")

        return pasos

    except Exception as e:
        print("💥 Error interno:", e)
        return ["Error: no se pudo procesar la ecuación"]

# 🌐 ESTE ERA EL QUE TE FALTABA
@app.route("/resolver", methods=["POST"])
def resolver():
    data = request.get_json()
    ecuacion = data.get("ecuacion", "")

    pasos = resolver_ecuacion(ecuacion)

    return jsonify({
        "pasos": pasos
    })

# 🚀 iniciar servidor
if __name__ == "__main__":
    app.run(debug=True)