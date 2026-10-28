"""Reproduce el chat de la parte B con la API de Ollama.

Equivale a las órdenes de parte_b_guia.txt: el mismo modelo, think apagado,
temperature 0, seed 42, num_ctx 512 y num_predict 1200. La API permite guardar
el historial, los tokens leídos (prompt_eval_count) y la respuesta completa.
No forma parte de los retos 1 a 4 como entrega de código: solo reproduce el chat.
"""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
URL = "http://127.0.0.1:11434/api/chat"

REGLA = "Regla: empieza SIEMPRE tu respuesta con «VEREDICTO:». ¿Entendido?"
SYSTEM = "Empieza SIEMPRE tu respuesta con «VEREDICTO:»."
Q1 = (
    "Explica en al menos 400 palabras cómo funciona el ingreso de un vehículo "
    "a ParqueFET: carné vigente, cupo de carros y motos, y cobro a visitantes."
)
Q2 = (
    "Explica en al menos 400 palabras cómo modelarías en una base de datos "
    "relacional los ingresos, las salidas y el cobro por hora o fracción de ParqueFET."
)


def chat(messages, system=None, num_ctx=512, num_predict=1200):
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.extend(messages)
    body = {
        "model": "qwen-demo",
        "messages": msgs,
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0,
            "seed": 42,
            "num_ctx": num_ctx,
            "num_predict": num_predict,
        },
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=900) as resp:
        return json.loads(resp.read().decode("utf-8"))


def texto(respuesta):
    msg = respuesta.get("message") or {}
    return msg.get("content") or ""


def bloque(titulo, respuesta):
    contenido = texto(respuesta).rstrip()
    palabras = len(contenido.split())
    return (
        f"## {titulo}\n\n"
        f"- prompt_eval_count: {respuesta.get('prompt_eval_count')}\n"
        f"- eval_count: {respuesta.get('eval_count')}\n"
        f"- palabras: {palabras}\n"
        f"- empieza_con_veredicto: {contenido.startswith('VEREDICTO:')}\n\n"
        f"{contenido}\n"
    )


def conversacion(system, primeros):
    mensajes = []
    partes = []
    for i, contenido in enumerate(primeros, start=1):
        mensajes.append({"role": "user", "content": contenido})
        respuesta = chat(mensajes, system=system)
        partes.append(bloque(f"Turno {i}", respuesta))
        mensajes.append({"role": "assistant", "content": texto(respuesta)})
        print(f"turno {i} prompt_eval={respuesta.get('prompt_eval_count')} eval={respuesta.get('eval_count')}", flush=True)
    return "\n".join(partes)


def main():
    print("version A", flush=True)
    a = conversacion(None, [REGLA, Q1, Q2])
    (ROOT / "salida_b_version_a.md").write_text(
        "# Parte B · versión A · regla como mensaje del chat\n\n"
        "Parámetros: qwen-demo, think false, temperature 0, seed 42, num_ctx 512, num_predict 1200.\n\n"
        + a,
        encoding="utf-8",
    )
    print("version B", flush=True)
    b = conversacion(SYSTEM, [Q1, Q2])
    (ROOT / "salida_b_version_b.md").write_text(
        "# Parte B · versión B · regla como system prompt\n\n"
        "Parámetros: qwen-demo, think false, temperature 0, seed 42, num_ctx 512, num_predict 1200.\n"
        "System: Empieza SIEMPRE tu respuesta con «VEREDICTO:».\n\n"
        + b,
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
