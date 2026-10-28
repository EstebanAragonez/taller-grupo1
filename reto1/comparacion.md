# Reto 1 · Comparación · ParqueFET

Modelo: `qwen-demo` (Qwen 3.5 4B, temperatura 0, semilla 42, `num_predict` 700 del Modelfile). Comando: `ollama run qwen-demo --think=false < reto1\prompt_....txt`.

La salida del prompt malo queda cortada en `###`. No es un cierre del modelo: el Modelfile de `qwen-demo` para a los 700 tokens. Aun así alcanza para ver qué inventó. Las otras dos salidas sí cierran el código.

## Decisiones que el prompt malo obligó a adivinar

El texto era solo «Hazme una función para registrar la entrada de un vehículo.» ParqueFET no aparece. El modelo resolvió por su cuenta:

1. **Lenguaje.** Entregó JavaScript ES6 y avisó que se podía pasar a Python, Java o C#. El backend del caso es Python.
2. **Datos de entrada.** Inventó `placa`, `modelo`, `color` y `horaEntrada`. No hay carné, ni tipo carro/moto, ni ocupación del parqueadero.
3. **Qué retorna.** Un objeto `{ exito, mensaje, datos }`, no una autorización de ingreso.
4. **Dónde se guarda.** Simula una base de datos, hace `console.log`, arma un `id` con `Date.now()` y un `timestamp` ISO. La función de ingreso no tiene por qué persistir.
5. **Reglas de negocio.** No usa ninguna: 120 carros, 300 motos, un vehículo por carné, registro más carné vigente, tarifa de visitante ni tope de 14 horas. El ejemplo de prueba es un Toyota Corolla rojo «en servicio», otro dominio.
6. **Forma de la respuesta.** Tutorial con encabezados, no una función lista para el backend. `vehiculoExiste = true` deja la verificación siempre en verde.

## Qué cumple la fórmula y antes no se cumplía

`prompt_formula.txt` separa los cinco bloques y mete las reglas en `<reglas>`. La función nueva:

- Se llama `puede_ingresar(vehiculo, ocupados)` y retorna `(bool, str)`.
- Rechaza si el vehículo no está registrado o el carné no está vigente.
- Rechaza si ese carné ya tiene otro vehículo adentro.
- Escribe el cupo como `>= 120` y `>= 300`. El borde es el correcto: con 120 carros no entra otro. La función con errores del caso usa `> 120` y deja pasar el carro 121.
- Rechaza tipo distinto de carro o moto, y un `ocupados` sin las claves, sin lanzar excepción en esos dos caminos.
- Deja el cobro y las 14 horas en el docstring, como fuera de alcance. No se los inventa como `if` de entrada. Eso respeta que esta firma no recibe la hora ni el medio de pago.

## Qué sigue fallando en la fórmula

El cupo no se aplica. El contexto dice que `ocupados` tiene las claves `"carros"` y `"motos"`, y que `tipo` vale `"carro"` o `"moto"`. La función comprueba que existan `"carros"` y `"motos"`, pero luego hace `ocupados.get(tipo, 0)` con `"carro"` o `"moto"`. Esa clave no está, el `.get` devuelve 0 y la comparación `0 >= 120` nunca es verdadera. Un parqueadero lleno entra igual.

Hay un segundo hueco, más chico: si falta la clave `tipo`, entra al rechazo de tipo inválido y ahí evalúa `vehiculo["tipo"]`, que sí lanza `KeyError`. La restricción pedía no lanzar excepciones.

Además trata `vehiculo` como `dict`. El enunciado hablaba de atributos (`vehiculo.carne_vigente` en la función del caso). El bloque de contexto no cerró esa elección. Y la respuesta va dentro de un bloque Markdown, aunque el formato pedía solo el código. El tope de 40 líneas tampoco se cumple: el docstring se come el presupuesto.

`es_visitante` no se usa. Aquí no es un error: el cobro quedó fuera de esta función a propósito.

## Qué cambió al quitar solo las restricciones

`prompt_variante.txt` es el mismo prompt sin el bloque `[RESTRICCIONES]`. Los otros cuatro bloques y las `<reglas>` siguen igual.

No apareció el cobro ni el control de 14 horas. Eso no lo sostenían las restricciones: lo sostenían «autoriza o niega el ingreso en este momento» y el hecho de que los parámetros no traen la hora. Quitar un bloque no borra los demás.

Lo que sí cambió es el guardarraíl:

- Aparece `from typing import Tuple, Dict, Literal`. El prompt ya no prohibía librerías.
- Desaparecen las validaciones de tipo inválido y de claves faltantes.
- El cupo sigue leyendo la clave equivocada (`"carro"` en vez de `"carros"`), pero ahora con `ocupados[tipo]`. Con los datos reales eso no falla abierto: lanza `KeyError`. El type hint lo deja por escrito, `Dict[Literal["carro", "moto"], int]`, en contra de las claves del contexto.
- El acceso directo `vehiculo["registrado"]` también lanza si falta el campo.

La fórmula y la variante aciertan las mismas reglas de negocio (registro, carné, un vehículo por carné, borde `>=`). La variante pierde el manejo de datos incompletos y convierte el bug del cupo en una excepción. Las restricciones no enseñaron las reglas; evitaron que una entrada mala rompiera la función.
