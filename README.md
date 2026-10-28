# Taller · Ingeniería de prompts y de contexto · ParqueFET

Diplomado en Ingeniería de Software con IA y Sistemas Agénticos · Sesión 03 · Módulo 1.

La carpeta sigue la estructura del taller.

`taller-grupo1`.

## Integrantes

Sergio Fernando Cardozo Chavarro.

Leonardo Esteban Aragonez Bobadilla.

Santiago Alarcon Vargas.

## Caso

**ParqueFET**, control del parqueadero del campus.

- Solo ingresan vehículos registrados a un carné vigente.
- Capacidad: 120 carros y 300 motos.
- Estudiantes y personal no pagan. Visitantes pagan $3.000 (carro) o $1.500 (moto) por hora o fracción.
- Un carné solo puede tener un vehículo dentro a la vez.
- Ningún vehículo puede permanecer más de 14 horas seguidas.

La función con errores de los retos 2 y 4 es `puede_ingresar`: rechaza el carné no vigente y, en carros, solo niega la entrada si `ocupados["carros"] > 120`. El requisito nuevo del reto 3 es que el visitante pague desde el celular antes de salir.

## Modelos y equipo

Ollama 0.40.12 en Windows. Comparaciones con temperatura 0 y semilla 42.

| Uso | Modelo |
| --- | --- |
| Retos 1, 2 (línea base), 3 y parte B del 4 | `qwen-demo` (`qwen3.5:4b`, `--think=false`) |
| Reto 2 | `revisor-parquefet` y `revisor-parquefet-v2`, creados con los Modelfile de `reto2/` |
| Reto 4, parte A | `phi-demo` (`phi4-mini`), sin `--think=false` |
| Bonus | `qwen3.5:4b` y `qwen3.5:0.8b` |

`qwen-demo` corta en 700 tokens (`num_predict` del Modelfile de la clase). En la parte B del reto 4 se subió a 1200 para que cada respuesta pudiera pasar de 400 palabras; si no, la regla de formato no sale de la ventana y el experimento no prueba el recorte.

## Cómo reproducir

Desde la raíz de esta carpeta, en el símbolo del sistema:

```bat
ollama create revisor-parquefet    -f reto2\Modelfile.v1
ollama create revisor-parquefet-v2 -f reto2\Modelfile.v2

ollama run qwen-demo --think=false < reto1\prompt_malo.txt
ollama run qwen-demo --think=false < reto1\prompt_formula.txt
ollama run qwen-demo --think=false < reto1\prompt_variante.txt
ollama run qwen-demo --think=false < reto2\prompt_revision.txt
ollama run revisor-parquefet --think=false < reto2\prompt_revision.txt
ollama run phi-demo < reto4\prompt_a_una_linea.txt
ollama run phi-demo < reto4\prompt_a_paso_a_paso.txt
```

Los ataques del reto 2 son `ataque_a_instrucciones.txt`, `ataque_b_directo.txt` y `ataque_c_comentario.txt`, cada uno contra los dos revisores. La parte B del reto 4 se reproduce con el chat de `parte_b_guia.txt` o con `py reto4\correr_parte_b.py` (la API local, con `num_ctx 512`). El bonus, desde `bonus/`:

```bat
uv sync
uv run reporte_json.py
uv run evalua.py
uv run evalua.py --modelo qwen3.5:0.8b
```

Las salidas guardadas están al lado de cada prompt. La nota de cada reto está en `reto1/comparacion.md`, `reto2/comparacion.md`, `reto3/nota_correccion.md`, `reto4/explicacion.md` y `bonus/analisis.md`.

## Reflexión

La técnica que más movió el resultado en ParqueFET fue dejar la regla escrita donde el modelo no tiene que inventarla. Sin reglas, `qwen-demo` reescribió `puede_ingresar` y conservó el `> 120`. Con el system prompt del revisor aparecieron el cupo de las motos, el borde de los 120 carros y el único vehículo por carné. En el bonus, el mismo modelo de 4B pasó de 4/10 a 10/10 cuando el prompt definió qué cuenta como ingreso, qué es una pregunta y qué es una alerta de permanencia. Con `qwen3.5:0.8b` ese texto solo subió de 4/10 a 5/10, y convirtió en RECHAZO una salida que la versión corta tenía bien: la definición no viaja sola.

Mañana, el pedido para programar el pago del visitante llevaría la firma, las reglas dentro de etiquetas, el momento (pagar antes de salir) y la cuenta de la hora o fracción. Esas reglas irían en el system prompt. En el reto 4 la misma orden, puesta como mensaje, desapareció en la segunda respuesta: la ventana de 512 se quedó solo con la pregunta. La traza con datos iría antes de aceptar un diagnóstico, porque `phi-demo` calculó que `120 > 120` es falso y concluyó que la función retorna falso. Y la tabla no se daría por buena hasta rehacer la multiplicación: 1 hora y 15 minutos en moto son $3.000, no $1.500.
