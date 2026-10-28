"""Parte A del bonus. Extrae notas del vigilante de ParqueFET a JSON con esquema.

    uv run reporte_json.py

Adaptado de scripts/reporte_json.py del kit de la clase.
"""
from typing import Literal

from pydantic import BaseModel, ValidationError

from comun import preguntar


class NotaPorteria(BaseModel):
    placa: str
    tipo: Literal["carro", "moto", "desconocido"]
    evento: Literal["entrada", "salida", "desconocido"]
    hora: str
    confianza: Literal["alta", "baja"]


NOTAS = [
    "Entró carro ABC123 a las 07:40. Carné de estudiante vigente.",
    "Salió la moto XYZ89 a las 18:05.",
    "Ingreso de visitante en carro, placa FET204, 09:15.",
    "Salida carro QWE456 a las 22:10. El vigilante anotó que superó las 14 horas.",
    "Dejaron una moto en la portería.",
    "El de la placa RTY321 otra vez, como a mediodía.",
]


INSTRUCCION = """Extrae los datos de una nota del vigilante de ParqueFET.
Si un dato no está en la nota, no lo inventes:
- placa u hora ausentes: cadena vacía
- tipo o evento ausentes o imposibles de decidir: "desconocido"
- confianza "baja" cuando falte o sea ambiguo alguno de placa, tipo, evento u hora; "alta" solo si los cuatro están explícitos.
<nota>{nota}</nota>"""


for texto in NOTAS:
    print("=" * 72)
    print("NOTA:", texto)
    r = preguntar(
        INSTRUCCION.format(nota=texto),
        formato=NotaPorteria.model_json_schema(),
        num_predict=200,
    )
    crudo = r.message.content
    print("JSON:", crudo)
    try:
        nota = NotaPorteria.model_validate_json(crudo)
    except ValidationError as e:
        print("NO CUMPLE EL ESQUEMA:")
        print(e)
        continue
    print(
        f"placa={nota.placa!r} | tipo={nota.tipo} | evento={nota.evento} | "
        f"hora={nota.hora!r} | confianza={nota.confianza}"
    )
