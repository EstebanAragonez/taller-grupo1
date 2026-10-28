"""Parte B del bonus. Compara dos prompts de clasificación sobre las mismas notas.

    uv run evalua.py
    uv run evalua.py --modelo qwen3.5:0.8b

Adaptado de scripts/evalua.py del kit de la clase.
Los casos marcados como ambiguos tienen una etiqueta decidida por el equipo:
el modelo no puede deducirla solo con el nombre de la categoría.
"""
import argparse
import re

from comun import preguntar

# (nota, etiqueta, es_ambiguo)
CASOS = [
    ("Entró el carro ABC123, estudiante, 07:42.", "INGRESO", False),
    ("Salió la moto XYZ89 a las 18:05.", "SALIDA", False),
    ("No dejé entrar el carro FER100: carné vencido.", "RECHAZO", False),
    ("Parqueadero de carros lleno. Devolví la placa TTT010.", "RECHAZO", False),
    ("¿A qué hora salió el carro de la placa QWE456?", "DUDA", False),
    # Ambiguo: hay pago y hay salida. El equipo etiqueta la operación, que es salir.
    ("El visitante de la camioneta FET204 pagó 9000 y se fue.", "SALIDA", True),
    # Ambiguo: alerta de permanencia. No confirma ingreso, salida ni rechazo.
    ("Lleva 15 horas el carro RTY321 adentro.", "DUDA", True),
    # Ambiguo: el ingreso ocurrió, pero falta la placa. El equipo lo cuenta como ingreso.
    ("Otra moto más en el sótano, no alcancé a anotar la placa.", "INGRESO", True),
    # Ambiguo: el estudiante y el sistema se contradicen.
    ("El estudiante dice que ya salió, pero el sistema lo muestra adentro.", "DUDA", True),
    ("Abrí la barrera y pasó el carro UUU777 a las 12:01.", "INGRESO", False),
]

V1 = """Clasifica la nota del vigilante de ParqueFET en UNA categoría: INGRESO, SALIDA, RECHAZO o DUDA.
Responde solo con la categoría.
Nota: "{nota}\""""

V2 = """Clasifica la nota del vigilante de ParqueFET en UNA categoría.
- INGRESO: el vigilante afirma que un vehículo entró o pasó la barrera, aunque falte la placa.
- SALIDA: el vigilante afirma que un vehículo salió o se fue, aunque también mencione el pago.
- RECHAZO: no se permitió el ingreso, se devolvió el vehículo o se bloqueó la entrada.
- DUDA: una pregunta, una alerta de permanencia o dos versiones contradictorias, sin una operación confirmada de entrar, salir o rechazar.

Ejemplo: "Lleva 16 horas el carro ABC adentro." -> DUDA
Ejemplo: "Pagó y se fue el carro XYZ." -> SALIDA
Ejemplo: "Entró una moto, no anoté la placa." -> INGRESO

Responde solo con INGRESO, SALIDA, RECHAZO o DUDA.
Nota: "{nota}\""""


def clasificar(plantilla, nota, modelo):
    r = preguntar(plantilla.format(nota=nota), modelo=modelo, num_predict=16)
    m = re.search(r"INGRESO|SALIDA|RECHAZO|DUDA", r.message.content.upper())
    return m.group(0) if m else r.message.content.strip()


ap = argparse.ArgumentParser()
ap.add_argument("--modelo", default="qwen3.5:4b")
a = ap.parse_args()
print(f"modelo: {a.modelo}")

for nombre, plantilla in [("v1", V1), ("v2", V2)]:
    ok = 0
    for nota, esperado, ambiguo in CASOS:
        obtenido = clasificar(plantilla, nota, a.modelo)
        marca = "ok" if obtenido == esperado else "FALLO"
        if obtenido == esperado:
            ok += 1
        amb = " ambiguo" if ambiguo else ""
        print(f"  [{nombre}] {marca}{amb}: «{nota}» -> {obtenido} (esperado {esperado})")
    print(f"{nombre}: {ok}/{len(CASOS)}\n")
