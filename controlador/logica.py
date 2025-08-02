from modelo.database import DatabaseManager

db = DatabaseManager()

def agregar_cuenta(nombre: str, tipo:str, balance: float) -> int:
    return db.insertar_cuenta(nombre, tipo, balance)

def obtener_cuentas():
    return db.obtener_cuentas()


def agregar_movimiento(fecha: str, tipo: str, categoria: str, descripcion: str, monto: float, cuenta_id: int, proyecto_id: int) -> int:
    return db.insertar_movimiento(fecha,tipo,categoria, descripcion, monto, cuenta_id, proyecto_id)

def obtener_movimientos():
    return db.obtener_movimientos()


def agregar_proyecto(nombre: str, meta: float, fecha_meta: str, descripcion: str) -> int:
    return db.insertar_proyecto(nombre, meta, fecha_meta, descripcion)

def obtener_proyectos():
    return db.obtener_proyectos()