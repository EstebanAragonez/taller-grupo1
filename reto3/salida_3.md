| Caso | Entrada | Resultado esperado | Criterio que cubre |
| :--- | :--- | :--- | :--- |
| 1 | Visitante en carro con estadía de 45 minutos | Cobrar $3.000 | Dado que soy un visitante registrado con vehículo en carro... |
| 2 | Visitante en moto con estadía de 1 hora y 15 minutos | Cobrar $1.500 | Dado que soy un visitante registrado con vehículo en moto... |
| 3 | Visitante en carro con estadía de 1 hora y 59 minutos | Cobrar $6.000 (2 horas) | Dado que mi estadía supera una hora completa pero no llega a dos... |
| 4 | Estudiante o personal con saldo cero | Mostrar mensaje de "no debo nada" y permitir salida | Dado que soy estudiante o personal registrado con monto cero en mi cuenta... |

**Nota:** Se revisó la cobertura de los criterios. Cada uno de los cuatro criterios proporcionados tiene al menos un caso de prueba asignado en la tabla anterior. No se agregaron casos nuevos, ya que todos los escenarios críticos (tipo de vehículo, duración específica y tipo de usuario con saldo cero) están representados.

