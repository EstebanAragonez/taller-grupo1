```python
from typing import Tuple, Dict, Literal

def puede_ingresar(
    vehiculo: dict, 
    ocupados: Dict[Literal["carro", "moto"], int]
) -> Tuple[bool, str]:
    """
    Determina si un vehículo puede ingresar al parqueadero según las reglas de negocio.

    Args:
        vehiculo (dict): Diccionario con los atributos del vehículo:
            - placa (str): Placa del vehículo.
            - tipo (Literal["carro", "moto"]): Tipo de vehículo.
            - registrado (bool): ¿Tiene carné registrado?
            - carne_vigente (bool): ¿El carné está vigente?
            - ya_hay_otro_vehiculo_del_carne (bool): ¿Ya hay otro vehículo del mismo carné dentro?
            - es_visitante (bool): ¿Es un visitante?
        ocupados (dict): Diccionario con las claves "carros" y "motos", indicando la cantidad de vehículos 
                        de ese tipo ya adentro.

    Returns:
        Tuple[bool, str]: Una tupla donde:
            - El primer elemento es True si puede ingresar, False en caso contrario.
            - El segundo elemento es "OK" si puede ingresar, o una frase descriptiva del motivo de rechazo.
    """
    
    # Regla 1: Solo ingresan vehículos registrados a un carné vigente.
    if not vehiculo["registrado"] or not vehiculo["carne_vigente"]:
        return False, "El vehículo no tiene carné registrado o el carné no está vigente."

    # Regla 2: Un carné solo puede tener un vehículo dentro a la vez.
    if vehiculo["ya_hay_otro_vehiculo_del_carne"]:
        return False, "Ya hay otro vehículo del mismo carné adentro."

    # Regla 3: Capacidad máxima (120 carros y 300 motos).
    tipo = vehiculo["tipo"]
    limite = {"carro": 120, "moto": 300}
    if ocupados[tipo] >= limite[tipo]:
        return False, f"El parqueadero está lleno de {tipo.lower()}."

    # Nota: Las reglas de pago y límite de tiempo (14 horas) no afectan la autorización de ingreso 
    # en este momento según el enunciado ("Autoriza o niega el ingreso... en este momento").
    # Se asume que se verifica el tiempo al salir, no al entrar.

    return True, "OK"
```

