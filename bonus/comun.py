"""Función común para hablar con Ollama. Adaptada de scripts/comun.py del kit de la clase."""
from ollama import chat, ResponseError

MODELO = "qwen3.5:4b"


def preguntar(contenido, modelo=MODELO, system=None, temperatura=0, seed=42,
              num_ctx=None, num_predict=None, formato=None, pensar=False, mensajes=None):
    """Envía un mensaje al modelo y devuelve la respuesta de Ollama."""
    if mensajes is None:
        mensajes = []
        if system:
            mensajes.append({"role": "system", "content": system})
        mensajes.append({"role": "user", "content": contenido})
    opciones = {"temperature": temperatura}
    if seed is not None:
        opciones["seed"] = seed
    if num_ctx:
        opciones["num_ctx"] = num_ctx
    if num_predict:
        opciones["num_predict"] = num_predict
    args = dict(model=modelo, messages=mensajes, options=opciones)
    if formato is not None:
        args["format"] = formato
    try:
        r = chat(think=pensar, **args)
    except ResponseError as e:
        if "think" in str(e).lower():
            r = chat(**args)
        else:
            raise
    return r
