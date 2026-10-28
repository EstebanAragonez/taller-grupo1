modelo: qwen3.5:0.8b
  [v1] FALLO: «Entró el carro ABC123, estudiante, 07:42.» -> SALIDA (esperado INGRESO)
  [v1] ok: «Salió la moto XYZ89 a las 18:05.» -> SALIDA (esperado SALIDA)
  [v1] ok: «No dejé entrar el carro FER100: carné vencido.» -> RECHAZO (esperado RECHAZO)
  [v1] ok: «Parqueadero de carros lleno. Devolví la placa TTT010.» -> RECHAZO (esperado RECHAZO)
  [v1] FALLO: «¿A qué hora salió el carro de la placa QWE456?» -> SALIDA (esperado DUDA)
  [v1] ok ambiguo: «El visitante de la camioneta FET204 pagó 9000 y se fue.» -> SALIDA (esperado SALIDA)
  [v1] FALLO ambiguo: «Lleva 15 horas el carro RTY321 adentro.» -> RECHAZO (esperado DUDA)
  [v1] FALLO ambiguo: «Otra moto más en el sótano, no alcancé a anotar la placa.» -> RECHAZO (esperado INGRESO)
  [v1] FALLO ambiguo: «El estudiante dice que ya salió, pero el sistema lo muestra adentro.» -> SALIDA (esperado DUDA)
  [v1] FALLO: «Abrí la barrera y pasó el carro UUU777 a las 12:01.» -> RECHAZO (esperado INGRESO)
v1: 4/10

  [v2] ok: «Entró el carro ABC123, estudiante, 07:42.» -> INGRESO (esperado INGRESO)
  [v2] FALLO: «Salió la moto XYZ89 a las 18:05.» -> RECHAZO (esperado SALIDA)
  [v2] ok: «No dejé entrar el carro FER100: carné vencido.» -> RECHAZO (esperado RECHAZO)
  [v2] ok: «Parqueadero de carros lleno. Devolví la placa TTT010.» -> RECHAZO (esperado RECHAZO)
  [v2] FALLO: «¿A qué hora salió el carro de la placa QWE456?» -> SALIDA (esperado DUDA)
  [v2] ok ambiguo: «El visitante de la camioneta FET204 pagó 9000 y se fue.» -> SALIDA (esperado SALIDA)
  [v2] FALLO ambiguo: «Lleva 15 horas el carro RTY321 adentro.» -> RECHAZO (esperado DUDA)
  [v2] FALLO ambiguo: «Otra moto más en el sótano, no alcancé a anotar la placa.» -> RECHAZO (esperado INGRESO)
  [v2] FALLO ambiguo: «El estudiante dice que ya salió, pero el sistema lo muestra adentro.» -> SALIDA (esperado DUDA)
  [v2] ok: «Abrí la barrera y pasó el carro UUU777 a las 12:01.» -> INGRESO (esperado INGRESO)
v2: 5/10

