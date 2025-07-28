from modelo.database import DatabaseManager

db = DatabaseManager()

def agregar_cuenta(nombre: str, tipo:str, balance: float) -> int:
    return db.insertar_cuenta(nombre, tipo, balance)

def obtener_cuentas():
    return db.obtener_cuentas()