CAMBIOS REQUERIDOS

**Hallazgos:**
1. **Línea 3-4:** Se omite la verificación de capacidad para motos (límite de 300).
2. **Línea 5:** Falta el bloque `else` para rechazar vehículos cuando hay cupo lleno, devolviendo explícitamente `False`.
3. **Línea 4:** No se valida si el carné tiene otro vehículo dentro (regla de exclusión por carné).
4. **Línea 5:** Se ignora la regla de límite de 14 horas de permanencia.

**Corrección sugerida:**
```python
def puede_ingresar(vehiculo, ocupados):
    if not vehiculo.carne_vigente: return False
    if vehiculo.tipo == "carro" and ocupados["carros"] >= 120: return False
    if vehiculo.tipo == "moto" and ocupados["motos"] >= 300: return False
    if len(vehiculo.vehiculos_actuales) > 0: return False # Carné ocupado
    if (hora_actual - vehiculo.hora_entrada).total_seconds() / 3600 > 14: return False
    return True
```

