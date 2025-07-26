from modelo.database import DatabaseManager

# Crear instancia de la base de datos
db = DatabaseManager()

print("✔ Base de datos creada y tablas listas.")

# (en el futuro aquí usarás insertar, consultar, etc.)


# Verificar qué tablas existen en la base de datos
db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = db.cursor.fetchall()

print("📋 Tablas encontradas en la base de datos:")
for tabla in tablas:
    print("   -", tabla[0])
