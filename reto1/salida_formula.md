```python
def puede_ingresar(vehiculo: dict, ocupados: dict) -> tuple[bool, str]:
    """
    Verifica si un vehículo puede ingresar al parqueadero según reglas de negocio.
    
    Reglas aplicadas:
    - Solo vehículos registrados con carné vigente.
    - Capacidad máxima: 120 carros y 300 motos.
    - Un carné solo tiene un vehículo activo a la vez (ya_hay_otro_vehiculo_del_carne).
    - Tipos válidos: "carro" o "moto".
    
    Reglas NO aplicadas en esta función (fuera de alcance):
    - Cobros por visitantes.
    - Tope de 14 horas de permanencia (requiere acceso a reloj/hora de entrada).
    
    Args:
        vehiculo: Diccionario con claves 'placa', 'tipo', 'registrado', 'carne_vigente', 
                  'ya_hay_otro_vehiculo_del_carne', 'es_visitante'.
        ocupados: Diccionario con claves 'carros' y 'motos' indicando cantidad actual.
    
    Returns:
        Tupla (bool, str): True y "OK" si puede entrar; False y motivo de rechazo.
    """
    # Validación básica de parámetros
    if not isinstance(vehiculo, dict) or not isinstance(ocupados, dict):
        return False, "Formato inválido de entrada"
    
    tipos_validos = {"carro", "moto"}
    if vehiculo.get("tipo") not in tipos_validos:
        return False, f"Tipo '{vehiculo['tipo']}' no válido"
    
    if "carros" not in ocupados or "motos" not in ocupados:
        return False, "Faltan claves en 'ocupados'"
    
    # Regla 1: Solo registrados con carné vigente
    if not vehiculo.get("registrado", False) or not vehiculo.get("carne_vigente", False):
        return False, "Vehículo no registrado o carné inválido"
    
    # Regla 2: Capacidad total
    tipo = vehiculo["tipo"]
    limite = {"carro": 120, "moto": 300}
    if ocupados.get(tipo, 0) >= limite[tipo]:
        return False, f"Llegó el límite de {tipo}s"
    
    # Regla 3: Un carné solo tiene un vehículo activo a la vez
    if vehiculo.get("ya_hay_otro_vehiculo_del_carne", False):
        return False, "El carné ya tiene un vehículo dentro"
    
    return True, "OK"
```

