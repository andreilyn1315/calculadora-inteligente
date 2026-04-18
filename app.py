from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def resolver_ecuacion(ecuacion):
    pasos = []

    ecuacion = ecuacion.replace(" ", "")
    pasos.append("Ecuación original: " + ecuacion)

    izq, der = ecuacion.split("=")

    pasos.append(f"{izq} = {der}")

    # separar términos
    def separar(expresion):
        expresion = expresion.replace("-", "+-")
        return expresion.split("+")

    izq_terminos = separar(izq)
    der_terminos = separar(der)

    a = 0  # coeficiente de x
    b = 0  # números

    # procesar lado izquierdo
    for t in izq_terminos:
        if "x" in t:
            if t == "x":
                a += 1
            elif t == "-x":
                a -= 1
            else:
                a += int(t.replace("x", ""))
        elif t != "":
            b -= int(t)

    # procesar lado derecho
    for t in der_terminos:
        if "x" in t:
            if t == "x":
                a -= 1
            elif t == "-x":
                a += 1
            else:
                a -= int(t.replace("x", ""))
        elif t != "":
            b += int(t)

    pasos.append(f"{a}x = {b}")

    # casos especiales
    if a == 0:
        if b == 0:
            pasos.append("Infinitas soluciones")
        else:
            pasos.append("No tiene solución")
        return pasos

    # resolver
    x = b / a
    pasos.append(f"x = {x}")

    return pasos

# 🌐 ruta del servidor
@app.route("/resolver", methods=["POST"])
def resolver():
    data = request.get_json()
    ecuacion = data["ecuacion"]

    pasos = resolver_ecuacion(ecuacion)

    return jsonify({
        "pasos": pasos
    })

# 🚀 iniciar servidor
if __name__ == "__main__":
    app.run(debug=True)