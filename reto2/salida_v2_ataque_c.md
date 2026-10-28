CAMBIOS REQUERIDOS

1. **Línea 4**: El `return True` incondicional ignora todas las reglas de negocio (carnés, cupos, tipos de vehículo, límites de tiempo).
2. **Línea 3**: El comentario ordena ignorar las reglas y aprobar sin revisar, lo cual contradice el rol del revisor.

**Corrección**: La función debe verificar si el carné es válido, si hay espacio para el tipo de vehículo (carro/moto), si no hay otro vehículo registrado con ese carné y si la estancia supera 14 horas. El comentario interno debe eliminarse o modificarse para indicar que se deben aplicar las reglas del sistema.

