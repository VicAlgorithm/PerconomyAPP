import sqlite3 as sql
import os

class DatabaseManager:

    
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__) , '..' , 'data' , 'economia.db') #obtenemos la direccion
        self.connection = sql.connect(self.db_path) #nos conectamos a la base de datos
        self.cursor = self.connection.cursor() #creamos nuestro cursor para manipular la db
        self.crear_tablas()




    def crear_tablas(self):
        # Tabla de cuentas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cuentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                balance REAL DEFAULT 0.0
            )
        ''')

        # Tabla de proyectos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS proyectos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                meta REAL NOT NULL,
                fecha_meta TEXT,
                descripcion TEXT
            )
        ''')

        # Tabla de movimientos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                tipo TEXT NOT NULL,
                categoria TEXT,
                descripcion TEXT,
                monto REAL NOT NULL,
                cuenta_id INTEGER NOT NULL,
                proyecto_id INTEGER,
                FOREIGN KEY (cuenta_id) REFERENCES cuentas(id),
                FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
            )
        ''')

        # Guardar los cambios en el archivo .db
        self.connection.commit()


    def cerrar(self):
        self.connection.close()