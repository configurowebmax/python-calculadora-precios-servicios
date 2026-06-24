"""
=====================================================================
 Calculadora de Precios de Servicios
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_calculadora_precios_servicios_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Calculadora de Precios de Servicios."""

    def __init__(self, costo, margen, iva):
        self.costo = float(costo)
        self.margen = float(margen)
        self.iva = float(iva)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        if self.margen >= 100:
            return {"error": "El margen no puede ser 100% o más."}
        base = self.costo / (1 - self.margen / 100)
        con_iva = base * (1 + self.iva / 100)
        ganancia = base - self.costo
        return {"base": base, "con_iva": con_iva, "ganancia": ganancia,
                "iva_monto": con_iva - base}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""
        return "✅ Precio calculado considerando costo, margen e impuesto."


# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("costo"), input_float("margen"), input_float("iva"))
    r = c.calcular()
    if "error" in r:
        mostrar(f'❌ {r["error"]}', clase="is-error"); return
    html = f"""
      <div class="result-value">💲 Precio final: {fmt_moneda(r["con_iva"])}</div>
      <p class="result-detail">Precio base: <strong>{fmt_moneda(r["base"])}</strong></p>
      <p class="result-detail">Ganancia: <strong>{fmt_moneda(r["ganancia"])}</strong></p>
      <p class="result-detail">IVA: <strong>{fmt_moneda(r["iva_monto"])}</strong></p>
      <p class="result-detail">{c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "costo": input_float("costo"),
            "margen": input_float("margen"),
            "iva": input_float("iva"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
            if "costo" in datos:
                document.querySelector("#costo").value = datos["costo"]
            if "margen" in datos:
                document.querySelector("#margen").value = datos["margen"]
            if "iva" in datos:
                document.querySelector("#iva").value = datos["iva"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
