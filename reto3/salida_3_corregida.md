| Caso | Entrada | Resultado esperado | Criterio que cubre |
|---|---|---|---|
| 1 | Visitante en carro, estadía de 1 hora y 15 minutos | Cuenta: 2 horas × $3.000 = $6.000 | Dado que soy un visitante registrado con vehículo en carro... |
| 2 | Visitante en moto, estadía de 1 hora y 45 minutos | Cuenta: 2 horas × $1.500 = $3.000 | Dado que soy un visitante registrado con vehículo en moto... |
| 3 | Visitante en carro, estadía de 1 hora y 59 minutos | Cuenta: 2 horas × $3.000 = $6.000 | Dado que mi estadía supera una hora completa pero no llega a dos... |
| 4 | Estudiante/personal, cuenta con saldo cero | Mensaje: "No debes nada", permite salida | Dado que soy estudiante o personal registrado con monto cero en mi cuenta... |

**Notas sobre los casos agregados:**
- Se agregaron los **Casos 1 y 2** para cubrir explícitamente las tarifas específicas de carro ($3.000) y moto ($1.500), ya que el criterio original solo especificaba la lógica de "hora o fracción" sin diferenciar el tipo de vehículo en el resultado numérico.
- Se agregó el **Caso 3** para reforzar el criterio de redondeo hacia arriba (una hora y 59 minutos se cobra como dos horas) con un ejemplo claro que evita la confusión del caso incorrecto mencionado en las instrucciones.
- Todos los montos calculados siguen la fórmula: `horas cobradas × tarifa = total`, donde una hora fraccionaria siempre se redondea a la siguiente hora completa.

