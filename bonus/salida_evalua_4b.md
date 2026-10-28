modelo: qwen3.5:4b
  [v1] ok: «Entró el carro ABC123, estudiante, 07:42.» -> INGRESO (esperado INGRESO)
  [v1] FALLO: «Salió la moto XYZ89 a las 18:05.» -> INGRESO (esperado SALIDA)
  [v1] FALLO: «No dejé entrar el carro FER100: carné vencido.» -> SALIDA (esperado RECHAZO)
  [v1] FALLO: «Parqueadero de carros lleno. Devolví la placa TTT010.» -> INGRESO (esperado RECHAZO)
  [v1] FALLO: «¿A qué hora salió el carro de la placa QWE456?» -> SALIDA (esperado DUDA)
  [v1] ok ambiguo: «El visitante de la camioneta FET204 pagó 9000 y se fue.» -> SALIDA (esperado SALIDA)
  [v1] FALLO ambiguo: «Lleva 15 horas el carro RTY321 adentro.» -> INGRESO (esperado DUDA)
  [v1] FALLO ambiguo: «Otra moto más en el sótano, no alcancé a anotar la placa.» -> DUDA (esperado INGRESO)
  [v1] ok ambiguo: «El estudiante dice que ya salió, pero el sistema lo muestra adentro.» -> DUDA (esperado DUDA)
  [v1] ok: «Abrí la barrera y pasó el carro UUU777 a las 12:01.» -> INGRESO (esperado INGRESO)
v1: 4/10

  [v2] ok: «Entró el carro ABC123, estudiante, 07:42.» -> INGRESO (esperado INGRESO)
  [v2] ok: «Salió la moto XYZ89 a las 18:05.» -> SALIDA (esperado SALIDA)
  [v2] ok: «No dejé entrar el carro FER100: carné vencido.» -> RECHAZO (esperado RECHAZO)
  [v2] ok: «Parqueadero de carros lleno. Devolví la placa TTT010.» -> RECHAZO (esperado RECHAZO)
  [v2] ok: «¿A qué hora salió el carro de la placa QWE456?» -> DUDA (esperado DUDA)
  [v2] ok ambiguo: «El visitante de la camioneta FET204 pagó 9000 y se fue.» -> SALIDA (esperado SALIDA)
  [v2] ok ambiguo: «Lleva 15 horas el carro RTY321 adentro.» -> DUDA (esperado DUDA)
  [v2] ok ambiguo: «Otra moto más en el sótano, no alcancé a anotar la placa.» -> INGRESO (esperado INGRESO)
  [v2] ok ambiguo: «El estudiante dice que ya salió, pero el sistema lo muestra adentro.» -> DUDA (esperado DUDA)
  [v2] ok: «Abrí la barrera y pasó el carro UUU777 a las 12:01.» -> INGRESO (esperado INGRESO)
v2: 10/10

