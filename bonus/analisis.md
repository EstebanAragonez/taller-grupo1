# Bonus · Análisis · ParqueFET

Parte A: `reporte_json.py` con `qwen3.5:4b`, temperatura 0, semilla 42 y el esquema de `NotaPorteria`. Parte B: `evalua.py` con los mismos diez casos en `qwen3.5:4b` y en `qwen3.5:0.8b`.

## Parte A · qué hace cuando falta un dato

El esquema no deja campos opcionales. Si el modelo omite una clave, Pydantic rechaza el JSON. Ninguno de los seis fue rechazado: siempre entregó las cinco claves. Cuando el dato no está, no lo deja en blanco por el esquema; lo llena con el centinela que pidió el prompt: `""` en placa u hora, `"desconocido"` en tipo o evento, y `confianza` `"baja"`.

| Nota | placa | tipo | evento | hora | confianza |
| --- | --- | --- | --- | --- | --- |
| Entró carro ABC123 a las 07:40 | ABC123 | desconocido | entrada | 07:40 | baja |
| Salió la moto XYZ89 a las 18:05 | XYZ89 | desconocido | desconocido | 18:05 | baja |
| Ingreso de visitante en carro, placa FET204, 09:15 | FET204 | carro | entrada | 09:15 | alta |
| Salida carro QWE456 a las 22:10 | QWE456 | desconocido | desconocido | 22:10 | baja |
| Dejaron una moto en la portería | (vacía) | desconocido | desconocido | (vacía) | baja |
| El de la placa RTY321 otra vez, como a mediodía | RTY321 | desconocido | desconocido | mediodía | baja |

En la nota incompleta («Dejaron una moto en la portería») no inventó placa ni hora. El evento sí es ambiguo: «dejaron» puede ser una entrada. La confianza baja es la señal útil.

Esa misma señal se enciende cuando el dato sí está y el modelo no lo lee. «Entró carro ABC123» trae el tipo y lo marcó `desconocido`. «Salió la moto» y «Salida carro» usan palabras del esquema (`salida`, `carro`, `moto`) y las dos quedaron en `desconocido`. La única nota con confianza alta es la que trae las cuatro piezas con palabras cercanas al esquema: carro, ingreso, placa, 09:15.

«desconocido» no separa «no vino en la nota» de «vino y no lo mapeé». El esquema garantiza la forma, no la lectura. En la última nota, «como a mediodía» se copió en `hora` en vez de dejarla vacía. La confianza baja advierte que esa hora no es un reloj.

## Parte B · qué falla en v1 y no en v2

Diez notas etiquetadas a mano. Cuatro son ambiguas y la etiqueta es decisión del equipo, no una deducción del nombre de la categoría: «pagó y se fue» es SALIDA, «lleva 15 horas» es DUDA, «entró una moto y no hay placa» es INGRESO, y las dos versiones contradictorias son DUDA.

`qwen3.5:4b`: v1 zero-shot **4/10**, v2 con definiciones y tres ejemplos **10/10**.

Los seis fallos de v1 desaparecen en v2:

- «Salió la moto…» estaba en INGRESO. Pasa a SALIDA.
- «No dejé entrar…» y «Devolví la placa…» no caían en RECHAZO. v1 no usó RECHAZO ni una vez.
- «¿A qué hora salió…?» estaba en SALIDA por el verbo de la pregunta. Pasa a DUDA.
- «Lleva 15 horas…» estaba en INGRESO. Pasa a DUDA.
- «Otra moto… no alcancé a anotar la placa» estaba en DUDA. Pasa a INGRESO, que es la decisión del equipo: el vigilante afirma que entró.

Los otros dos ambiguos («pagó y se fue», «dice que salió pero el sistema lo muestra adentro») v1 ya los tenía bien, y v2 los conserva.

`qwen3.5:0.8b`: v1 **4/10**, v2 **5/10**. El mismo texto casi no se cobra. v2 corrige dos ingresos que v1 había perdido («Entró el carro ABC123» y «Abrí la barrera») y daña uno que v1 tenía bien: «Salió la moto XYZ89» pasa de SALIDA a RECHAZO. La pregunta por la hora, la alerta de 15 horas, la moto sin placa y la contradicción siguen mal. En el modelo chico, repetir RECHAZO en las definiciones no enseña el corte: lo empuja a esa etiqueta.

Lo que v1 no resuelve y v2 sí, en el 4B, son los casos donde el verbo engaña (una pregunta con «salió», un rechazo que no dice «salida», una alerta de permanencia, un ingreso sin placa). Hace falta decir qué cuenta cada categoría. En el 0.8B esas definiciones no alcanzan: el fallo de v1 que v2 no arregla es justo el caso ambiguo, más un caso claro que v2 empeora.
