import sqlite3 as sql  
import os

class DatabaseManager:
    """
    Manejador de base de datos SQLite para cuentas, proyectos y movimientos.

    Esta clase se encarga de conectar con el archivo .db, garantizar la creación
    del esquema y proporcionar métodos CRUD básicos para las tablas:
    - cuentas(id, nombre, tipo, balance)
    - proyectos(id, nombre, meta, fecha_meta, descripcion)
    - movimientos(id, fecha, tipo, categoria, descripcion, monto, cuenta_id, proyecto_id)

    """
    
    def __init__(self) -> None:
        """
        Inicializa la conexión y crea las tablas si no existen.

        """
        # Construir ruta al archivo .db (un nivel arriba de este script, carpeta 'data')
        self.db_path = os.path.join(os.path.dirname(__file__) , '..' , 'data' , 'economia.db')
        
        # Conectar a SQLite (crea el archivo si no existe)
        self.connection = sql.connect(self.db_path) 
        self.cursor = self.connection.cursor() 
        
        # Crear el esquema de tablas
        self.crear_tablas()



    
    def crear_tablas(self) -> None:
        """
        Crea las tablas necesarias si no existen.

        Tablas:
        - cuentas(id, nombre, tipo, balance)
        - proyectos(id, nombre, meta, fecha_meta, descripcion)
        - movimientos(id, fecha, tipo, categoria, descripcion, monto, cuenta_id, proyecto_id)
        """

        # Tabla de cuentas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cuentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                balance REAL NOT NULL
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

        self.connection.commit()



    def insertar_cuenta(self, nombre: str, tipo: str, balance: float = 0.0) -> int:
        """
        Inserta una nueva cuenta en la tabla 'cuentas'.

        Parameters
        ----------
        nombre : str
            Nombre descriptivo de la cuenta.
        tipo : str
            Categoría de la cuenta ('ahorro', 'gasto', etc.).
        balance : float
            Saldo inicial de la cuenta, por defecto 0.0.

        Returns
        -------
        int
            ID autogenerado de la nueva cuenta.
        """
        self.cursor.execute('INSERT INTO cuentas (nombre, tipo, balance) VALUES (?, ?, ?)',(nombre, tipo, balance))
        self.connection.commit()
        return self.cursor.lastrowid 



    def obtener_cuentas(self) -> list:
        """
        Recupera todas las filas de la tabla 'cuentas'.

        Returns
        -------
        list of tuple
            Lista de tuplas con (id, nombre, tipo, balance).
        """
        self.cursor.execute("SELECT * FROM cuentas")
        return self.cursor.fetchall()
    



    def insertar_movimiento(self, fecha: str, tipo: str, categoria: str, descripcion: str, monto: float, cuenta_id: int, proyecto_id: int = None) -> int:
        """
        Inserta un nuevo movimiento en la tabla 'movimientos'.

        Parameters
        ----------
        fecha : str
            Fecha de la operación (formato ISO, p. ej. 'YYYY-MM-DD').
        tipo : str
            Tipo de movimiento ('ingreso', 'egreso').
        categoria : str
            Categoría del movimiento (opcional).
        descripcion : str
            Descripción detallada (opcional).
        monto : float
            Cantidad asociada al movimiento.
        cuenta_id : int
            ID de la cuenta asociada (clave foránea).
        proyecto_id : int, optional
            ID de proyecto asociado (clave foránea), por defecto None.

        Returns
        -------
        int
            ID autogenerado del nuevo movimiento.
        """
        self.cursor.execute('INSERT INTO movimientos (fecha, tipo, categoria, descripcion, monto, cuenta_id, proyecto_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                            (fecha, tipo, categoria, descripcion, monto, cuenta_id, proyecto_id))
        self.connection.commit()
        return self.cursor.lastrowid
    


    def obtener_movimientos(self) -> list:
        """
        Recupera todas las filas de la tabla 'movimientos'.

        Returns
        -------
        list of tuple
            Lista de tuplas con los campos de movimientos.
        """
        self.cursor.execute('SELECT * FROM movimientos')
        return self.cursor.fetchall()



    def insertar_proyecto(self, nombre: str, meta: float, fecha_meta: str, descripcion: str) -> int:
        """
        Inserta un nuevo proyecto en la tabla 'proyectos'.

        Parameters
        ----------
        nombre : str
            Nombre del proyecto.
        meta : float
            Meta cuantitativa del proyecto.
        fecha_meta : str
            Fecha límite del proyecto (opcional).
        descripcion : str
            Descripción detallada del proyecto (opcional).

        Returns
        -------
        int
            ID autogenerado del nuevo proyecto.
        """
        self.cursor.execute('INSERT INTO proyectos (nombre, meta, fecha_meta, descripcion) VALUES (?, ?, ?, ?)',
                            (nombre, meta, fecha_meta, descripcion))
        self.connection.commit()
        return self.cursor.lastrowid
    

    
    def obtener_proyectos(self) -> list:
        """
        Recupera todas las filas de la tabla 'proyectos'.

        Returns
        -------
        list of tuple
            Lista de tuplas con los campos de proyectos.
        """
        self.cursor.execute('SELECT * FROM proyectos')
        return self.cursor.fetchall()



    def cerrar(self) -> None:
        """
        Cierra la conexión a la base de datos.
        """
        self.connection.close()