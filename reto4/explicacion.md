# Reto 4 · Qué pasó en cada parte

Referencias: práctica 9 (cadena de pensamiento con `phi-demo`) y práctica 14B (la instrucción que se olvida). Caso: ParqueFET. La función es la del enunciado, con `> 120`.

## Parte A · phi-demo, con los mismos datos

Datos: `carne_vigente = True`, `tipo = "carro"`, `ocupados["carros"] = 120`. Con la capacidad en 120, ese carro no debe entrar. La función lo deja entrar porque `120 > 120` es falso, el segundo `if` no retorna, y cae en `return True`.

`phi-demo` no tiene modo de razonamiento. Por eso no lleva `--think=false`. Lo que se compara es pedir la causa en una línea contra pedir la traza.

### Una línea · 0 errores

`salida_a_una_linea.md` dice: «Probablemente no se detectó el carné vigente o el tipo del vehículo.»

Los datos dicen lo contrario: el carné está vigente y el tipo es carro. No nombra el `>`, ni las 300 motos, ni el vehículo por carné. Errores reales de la función: cero. Causas inventadas: una.

### Paso a paso · el predicado sale bien y la conclusión no

`salida_a_paso_a_paso.md` escribe los dos valores:

- `not True` es `False`. Correcto.
- `120 > 120` es `False`. Correcto. Ese es el dato del bug.

En los dos `if` concluye que la función retorna `False`. Eso es otro error, de control de flujo: si la condición es falsa, el cuerpo no se ejecuta. Nunca llega a decir que el flujo cae en `return True`, que es por donde el carro entra.

El parche agrega `if ocupados["carros"] >= 120` y deja el `> 120` original. El borde quedaría cubierto de casualidad. El párrafo final vuelve a culpar al carné: «el carro aún no puede ingresar debido a la falta de una licencia válida». Los datos dicen que la licencia está vigente.

Errores de la función señalados y sostenidos hasta el final: cero en las dos versiones. La diferencia está en la traza. La de una línea no deja un dato que se pueda revisar. La larga deja `120 > 120` es `False` escrito al lado de una conclusión que lo contradice. Con phi-demo, pedir los pasos no garantiza el diagnóstico: garantiza que el valor quede a la vista. Quien lee la traza puede corregir al modelo. Quien lee la línea, no.

## Parte B · ventana de 512 y la regla «VEREDICTO:»

Regla propia del caso, el veredicto al inicio, como sugiere el taller. Preguntas de ParqueFET, cada una pidiendo al menos 400 palabras. `qwen-demo`, pensamiento apagado, temperatura 0, semilla 42.

`qwen-demo` trae `num_predict 700`. Una respuesta de 400 palabras no cabe en 700 tokens con margen, y si la primera respuesta queda corta la regla sigue en la ventana y la segunda la imita. Se subió `num_predict` a 1200, que en el chat es `/set parameter num_predict 1200`, y `num_ctx` a 512. El chat de la práctica es interactivo; aquí se reprodujo con la API local de Ollama, el mismo modelo y los mismos parámetros, para guardar cada turno y los tokens que el modelo realmente leyó (`prompt_eval_count`). El script está en `correr_parte_b.py`. Las órdenes de chat equivalentes están en `parte_b_guia.txt`.

Ollama, cuando el historial no cabe, bota mensajes enteros desde el más viejo. Conserva el último mensaje y, si existe, el system prompt.

### Versión A · la regla es un mensaje

| Turno | Qué se envió | Tokens leídos | Palabras | ¿Empieza en VEREDICTO:? |
| --- | --- | --- | --- | --- |
| 1 | La regla | 33 | 20 | Sí |
| 2 | Pregunta del ingreso | 119 | 552 | Sí |
| 3 | Pregunta de la base de datos | 53 | 482 | No |

En el turno 3 el modelo leyó 53 tokens. La pregunta sola pesa eso. No leyó la regla (33) ni la primera respuesta (723 tokens generados). Las dos se cayeron de la ventana de 512. Por eso la segunda respuesta larga ya no abre con `VEREDICTO:`. No es que el modelo «se haya distraído»: la instrucción ya no estaba.

### Versión B · la misma regla es el system prompt

Se hizo `/clear` (historial nuevo) y `/set system`.

| Turno | Tokens leídos | Palabras | ¿Empieza en VEREDICTO:? |
| --- | --- | --- | --- |
| 1 | 71 | 581 | Sí |
| 2 | 73 | 638 | Sí |

El turno 2 leyó 73 tokens, no los 752 de la primera respuesta. La respuesta larga también se botó. Lo que no se bota es el system prompt: 73 es la pregunta (los 53 de la versión A) más la regla. Las dos respuestas abren con `VEREDICTO:`.

La regla que tiene que cumplirse siempre no va en el primer mensaje del chat. Va en el system prompt, que la ventana no descarta. En un agente que trabaja un rato largo, lo mismo: las reglas del parqueadero viven en el system prompt o en una nota que se vuelve a inyectar, no en un turno que el recorte va a tirar.

Una salvedad, para no confundir formato con conocimiento. Ninguna de las cuatro respuestas largas usa las cifras de ParqueFET (120 carros, 300 motos, $3.000 y $1.500). Las preguntas no las traían, y el modelo se inventó un parque natural, con membresía y senderos. Obedecer `VEREDICTO:` no significa que el contenido sea el del campus. Esas cifras hay que volver a ponerlas en el mensaje que sí entra en la ventana, o en el mismo system prompt.
