# Reto 3 · Qué paso se corrigió y por qué

Cadena: historia (few-shot) → criterios Dado/Cuando/Entonces → tabla de casos con auto-verificación. Modelo `qwen-demo`, `--think=false`. La salida de cada paso entra al siguiente dentro de etiquetas.

## Paso 1 · no hubo que tocarlo

`salida_1.md` copia el formato de los dos ejemplos propios:

> Como visitante, quiero poder realizar el pago desde mi dispositivo móvil antes de salir del parqueadero, para evitar filas en la portería y agilizar mi salida sin necesidad de esperar a ser atendido manualmente.

El rol es el visitante, la acción es pagar desde el celular y el momento es antes de salir. El beneficio («evitar filas») no está en el requisito; es una inferencia razonable, no una regla de cobro. Este paso se dejó igual.

## El primer error apareció en el paso 2

`prompt_2_criterios.txt` pedía de 3 a 5 criterios, formato en tres líneas, y las reglas dentro de `<reglas>`, con la historia dentro de `<historia>`. `salida_2.md` falló en el primer criterio, y el fallo se repite en los cinco:

- Los cinco dicen «cuando intento ingresar». La historia dice «antes de salir». El modelo movió el pago a la entrada.
- No aparece la tarifa: ni $3.000, ni $1.500, ni la hora o fracción.
- El criterio 5 invierte el tope de 14 horas: impide pagar. Quien se quedó de más es justo quien tiene que pagar.
- Inventa «pago activo» y lo mezcla con la regla de un vehículo por carné.
- El formato pedido (tres líneas por criterio) sale en una sola línea.

Las reglas del bloque están escritas como reglas de ingreso. El modelo las usó como plantilla y tapó con ellas la historia, que era de salida. Por eso el arreglo no fue «pedir más criterios». Fue cambiar el momento, la tarifa y el formato en `prompt_2_corregido.txt`.

## Después de corregir el paso 2

`salida_2_corregida.md` ya no usa «ingresar». Cobra $3.000 al carro y $1.500 a la moto, cobra dos horas si la estadía pasa de una y no llega a dos, y al estudiante o al personal le muestra que no debe nada y lo deja salir. No bloquea el pago a las 14 horas. Quedan cuatro criterios, dentro del rango. Hay un «cobraré» en vez de «cobrará» en el tercero: se dejó, porque la cadena usa la salida tal cual.

Esa salida, sin editar, es el contenido de `<criterios>` en el paso 3.

## Lo que el paso 3 hizo con esos criterios

`salida_3.md` tiene las cuatro columnas y la auto-verificación: dice que cada criterio tiene un caso y que no agregó ninguno. La cobertura es cierta. La cuenta no:

| Caso de esa tabla | Estadía | Lo que escribió | Lo que corresponde |
| --- | --- | --- | --- |
| Moto | 1 h 15 min | $1.500 | 2 × $1.500 = $3.000 |
| Carro | 1 h 59 min | $6.000 | 2 × $3.000 = $6.000 |

El caso del carro con fracción está bien. El de la moto cobra la tarifa de una hora. La auto-verificación miró si había un caso por criterio, no si el monto era el de la regla. Por eso un «ya revisé» no alcanza: hay que decir qué se revisa.

`prompt_3_corregido.txt` obliga a escribir `horas cobradas × tarifa = total` y le muestra la cuenta mal hecha para que no la repita. `salida_3_corregida.md`:

- Carro, 1 h 15 min: 2 × $3.000 = $6.000.
- Moto, 1 h 45 min: 2 × $1.500 = $3.000.
- Carro, 1 h 59 min: 2 × $3.000 = $6.000.
- Estudiante o personal: mensaje de que no debe nada y puede salir.

Los cuatro criterios quedan cubiertos y las tres cuentas cierran. La nota del modelo dice que «agregó» los casos 1, 2 y 3. No los agregó: cada uno cubre un criterio que ya venía. La auto-verificación sigue teniendo un reflejo de anunciar agregados aunque la tabla esté completa. El monto, que era el error, sí quedó corregido.
