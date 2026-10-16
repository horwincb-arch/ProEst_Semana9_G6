import os

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_wtf.csrf import CSRFProtect

from pila import Pila


# ==================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ==================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY",
    "clave-desarrollo-cambiar-en-produccion",
)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

csrf = CSRFProtect(app)


# ==================================================
# CONSTANTES
# ==================================================

CAPACIDAD_MAXIMA = 20
CAPACIDAD_INICIAL = 5
LONGITUD_MAXIMA_ELEMENTO = 50


# ==================================================
# FUNCIONES AUXILIARES
# ==================================================

def obtener_pila() -> Pila:
    """Recupera la pila del visitante actual."""

    elementos = session.get("elementos", [])
    capacidad = session.get("capacidad", CAPACIDAD_INICIAL)

    return Pila(
        capacidad=capacidad,
        elementos=elementos,
    )


def guardar_pila(pila: Pila) -> None:
    """Guarda la pila en la sesión del visitante."""

    session["elementos"] = pila.obtener_elementos()
    session["capacidad"] = pila.capacidad


# ==================================================
# RUTA PRINCIPAL
# ==================================================

@app.route("/", methods=["GET"])
def inicio():
    """Muestra la página principal."""

    pila = obtener_pila()

    return render_template(
        "index.html",
        elementos=list(reversed(pila.obtener_elementos())),
        cantidad=pila.cantidad(),
        capacidad=pila.capacidad,
        tope=pila.ver_tope(),
        esta_vacia=pila.esta_vacia(),
        esta_llena=pila.esta_llena(),
        longitud_maxima=LONGITUD_MAXIMA_ELEMENTO,
    )


# ==================================================
# APILAR ELEMENTOS
# ==================================================

@app.route("/apilar", methods=["POST"])
def apilar():
    """Agrega un elemento a la pila."""

    elemento = request.form.get("elemento", "")

    if not isinstance(elemento, str):
        flash("El elemento proporcionado no es válido.", "danger")
        return redirect(url_for("inicio"))

    elemento = elemento.strip()

    if not elemento:
        flash("Debes escribir un elemento.", "warning")
        return redirect(url_for("inicio"))

    if len(elemento) > LONGITUD_MAXIMA_ELEMENTO:
        flash(
            f"El elemento no puede superar "
            f"{LONGITUD_MAXIMA_ELEMENTO} caracteres.",
            "warning",
        )
        return redirect(url_for("inicio"))

    pila = obtener_pila()

    if pila.esta_llena():
        flash("La pila está llena. No puedes agregar más elementos.", "warning")
        return redirect(url_for("inicio"))

    try:
        pila.apilar(elemento)
        guardar_pila(pila)

        flash(f"Se agregó '{elemento}' correctamente.", "success")

    except (ValueError, OverflowError) as error:
        flash(str(error), "danger")

    return redirect(url_for("inicio"))


# ==================================================
# DESAPILAR ELEMENTOS
# ==================================================

@app.route("/desapilar", methods=["POST"])
def desapilar():
    """Retira el elemento situado en el tope."""

    pila = obtener_pila()

    if pila.esta_vacia():
        flash("La pila está vacía. No hay elementos que retirar.", "warning")
        return redirect(url_for("inicio"))

    elemento = pila.desapilar()
    guardar_pila(pila)

    flash(f"Se retiró '{elemento}' correctamente.", "success")

    return redirect(url_for("inicio"))


# ==================================================
# VACIAR LA PILA
# ==================================================

@app.route("/limpiar", methods=["POST"])
def limpiar():
    """Elimina todos los elementos de la pila."""

    pila = obtener_pila()
    pila.limpiar()

    guardar_pila(pila)

    flash("La pila se vació correctamente.", "success")

    return redirect(url_for("inicio"))


# ==================================================
# EJECUCIÓN DE LA APLICACIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)