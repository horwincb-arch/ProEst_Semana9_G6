import os
import secrets
from io import BytesIO
from pathlib import Path

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_wtf.csrf import CSRFProtect
from PIL import Image, UnidentifiedImageError

from pila import Pila


# ==================================================
# CONFIGURACIÓN
# ==================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY",
    secrets.token_hex(32),
)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

CSRFProtect(app)

BASE_DIR = Path(__file__).resolve().parent
CARPETA_FOTOGRAFIAS = BASE_DIR / "uploads"

CARPETA_FOTOGRAFIAS.mkdir(parents=True, exist_ok=True)

CAPACIDAD_PILA = 20
TAMANO_MAXIMO = 5 * 1024 * 1024

FORMATOS_PERMITIDOS = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "WEBP": ".webp",
}


# ==================================================
# FUNCIONES AUXILIARES
# ==================================================

def obtener_pila() -> Pila:
    """Recupera la pila de fotografías de la sesión actual."""

    fotografias = session.get("fotografias", [])

    return Pila(
        capacidad=CAPACIDAD_PILA,
        elementos=fotografias,
    )


def guardar_pila(pila: Pila) -> None:
    """Guarda las referencias de las fotografías en la sesión."""

    session["fotografias"] = pila.obtener_elementos()


def validar_fotografia(contenido: bytes) -> str | None:
    """Valida el contenido real de una imagen."""

    if not contenido or len(contenido) > TAMANO_MAXIMO:
        return None

    try:
        with Image.open(BytesIO(contenido)) as imagen:
            formato = imagen.format

            if formato not in FORMATOS_PERMITIDOS:
                return None

            imagen.verify()

        return FORMATOS_PERMITIDOS[formato]

    except (UnidentifiedImageError, OSError, ValueError):
        return None


def eliminar_archivo(nombre_archivo: str) -> None:
    """Elimina una fotografía de la carpeta de almacenamiento."""

    ruta = CARPETA_FOTOGRAFIAS / nombre_archivo

    try:
        ruta.resolve().relative_to(CARPETA_FOTOGRAFIAS.resolve())
    except ValueError:
        return

    if ruta.is_file():
        ruta.unlink()


# ==================================================
# PÁGINA PRINCIPAL
# ==================================================

@app.route("/", methods=["GET"])
def inicio():
    """Muestra la pila de fotografías."""

    pila = obtener_pila()

    return render_template(
        "index.html",
        fotografias=list(reversed(pila.obtener_elementos())),
        cantidad=pila.cantidad(),
        capacidad=pila.capacidad,
        esta_vacia=pila.esta_vacia(),
        esta_llena=pila.esta_llena(),
        tope=pila.ver_tope(),
    )


# ==================================================
# APILAR FOTOGRAFÍA
# ==================================================

@app.route("/apilar", methods=["POST"])
def apilar():
    """Valida, guarda y apila una fotografía."""

    pila = obtener_pila()

    if pila.esta_llena():
        flash("La pila está llena.", "warning")
        return redirect(url_for("inicio"))

    archivo = request.files.get("fotografia")

    if archivo is None or not archivo.filename:
        flash("Debes capturar una fotografía primero.", "warning")
        return redirect(url_for("inicio"))

    contenido = archivo.read(TAMANO_MAXIMO + 1)
    extension = validar_fotografia(contenido)

    if extension is None:
        flash(
            "La imagen no es válida o supera los 5 MB permitidos.",
            "warning",
        )
        return redirect(url_for("inicio"))

    nombre_archivo = f"{secrets.token_hex(16)}{extension}"
    ruta_archivo = CARPETA_FOTOGRAFIAS / nombre_archivo

    try:
        with ruta_archivo.open("xb") as destino:
            destino.write(contenido)

        pila.apilar(nombre_archivo)
        guardar_pila(pila)

        flash("Fotografía agregada correctamente.", "success")

    except (OSError, ValueError, OverflowError):
        eliminar_archivo(nombre_archivo)

        app.logger.exception("Error al guardar una fotografía.")

        flash("No se pudo guardar la fotografía.", "danger")

    return redirect(url_for("inicio"))


# ==================================================
# DESAPILAR FOTOGRAFÍA
# ==================================================

@app.route("/desapilar", methods=["POST"])
def desapilar():
    """Retira la fotografía situada en el tope."""

    pila = obtener_pila()

    if pila.esta_vacia():
        flash("La pila está vacía.", "warning")
        return redirect(url_for("inicio"))

    nombre_archivo = pila.desapilar()
    guardar_pila(pila)

    try:
        eliminar_archivo(nombre_archivo)
    except OSError:
        app.logger.exception("No se pudo eliminar la fotografía.")

    flash("Se retiró la última fotografía.", "success")

    return redirect(url_for("inicio"))


# ==================================================
# VACIAR PILA
# ==================================================

@app.route("/limpiar", methods=["POST"])
def limpiar():
    """Retira todas las fotografías de la pila."""

    pila = obtener_pila()
    fotografias = pila.limpiar()

    guardar_pila(pila)

    for nombre_archivo in fotografias:
        try:
            eliminar_archivo(nombre_archivo)
        except OSError:
            app.logger.exception(
                "No se pudo eliminar una fotografía."
            )

    flash("La pila se vació correctamente.", "success")

    return redirect(url_for("inicio"))


# ==================================================
# MOSTRAR FOTOGRAFÍA
# ==================================================

@app.route("/fotografias/<nombre_archivo>", methods=["GET"])
def mostrar_fotografia(nombre_archivo):
    """Muestra una imagen que pertenece a la pila de la sesión."""

    pila = obtener_pila()

    if nombre_archivo not in pila.obtener_elementos():
        abort(404)

    return send_from_directory(
        CARPETA_FOTOGRAFIAS,
        nombre_archivo,
        as_attachment=False,
    )


# ==================================================
# MANEJO DEL TAMAÑO DE SOLICITUD
# ==================================================

@app.errorhandler(413)
def archivo_demasiado_grande(error):
    """Informa cuando una solicitud supera el límite permitido."""

    flash("La solicitud supera el tamaño máximo permitido.", "warning")

    return redirect(url_for("inicio"))


# ==================================================
# EJECUCIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)