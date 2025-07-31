import tkinter as tk
from tkinter import messagebox
from controlador.logica import *

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("PerconomyApp - Economía Personal")
        self.root.geometry("700x400")
        self.root.minsize(700,500)
        self.root.maxsize(700,500)

        # 🔹 Crear contenedor principal
        self.contenedor = tk.Frame(self.root,  bg= "light yellow")
        self.contenedor.pack(fill="both", expand=True)

        # 🔹 Crear el panel lateral pero no lo mostramos todavía
        self.menu_lateral = tk.Frame(self.contenedor, bg="DeepSkyBlue4", width=200)
        self.menu_visible = False  # Controla si está visible o no
        self.menu_lateral.lift()

        self.nomenu_lateral = tk.Frame(self.contenedor, bg="DeepSkyBlue4", width=45)
        self.nomenu_lateral.pack(side="left", fill="y")
        self.nomenu_visible = True
        self.nomenu_lateral.lift()

        # 🔹 Botón con ícono para abrir/cerrar el menú
        self.icono_menu = tk.PhotoImage(file="a.png").subsample(30, 30)
        self.btn_menu = tk.Button(self.contenedor, image=self.icono_menu,  bg= "lightyellow2", command=self.toggle_menu)
        self.btn_menu.place(x=1, y=1)

        self.TextoInicial = tk.Label(self.contenedor, text="PerconomyAPP", bg="light yellow", font=("Arial", 24, "bold"))
        self.TextoInicial.place(relx=0.5, rely=0.2, anchor="center")

        self.zona_agregar_cuenta = tk.Frame(self.contenedor, bg="light yellow")  
        self.zona_ver_cuentas = tk.Frame(self.contenedor, bg="light yellow")  

    def toggle_menu(self):
        if self.menu_visible:
            self.animar_cerrar()
        else:
            self.nomenu_lateral.pack_forget()
            self.menu_lateral.place(x=0, y=0, width=0, height= 500)
            self.animar_abrir()
            self.nomenu_visible = False
    
    def animar_abrir(self, ancho=0):
        if ancho <= 200:
            self.menu_lateral.place(x=0, y=0, width=ancho, height= 500)
            self.btn_menu.place(x=ancho +5, y=1)
            self.btn_menu.lift()
            self.actualizar_posicion_titulo()
            self.root.after(5, lambda: self.animar_abrir(ancho +10))
        else:
            self.menu_visible = True
            self.agregar_botones_menu()
            self.actualizar_posicion_titulo()

    def animar_cerrar(self, ancho = 200):
        if ancho >= 45:
            self.menu_lateral.place(x=0, y=0, width=ancho, height=500)
            self.btn_menu.place(x=ancho + 5, y=1)
            self.btn_menu.lift()
            self.actualizar_posicion_titulo()
            self.root.after(5, lambda: self.animar_cerrar(ancho-10))
        else:
            self.menu_lateral.place_forget()
            self.nomenu_lateral.pack(side="left", fill="y")
            self.btn_menu.place(x=1, y=1)
            self.menu_visible = False
            self.nomenu_visible = True
            self.actualizar_posicion_titulo()
            

    def actualizar_posicion_titulo(self):
        if self.menu_visible:
            self.TextoInicial.place(relx=0.65, rely=0.2, anchor="center")
        else:
            self.TextoInicial.place(relx=0.5, rely=0.2, anchor="center")



    def agregar_botones_menu(self):
        for widget in self.menu_lateral.winfo_children():
            widget.destroy()

        tk.Label(self.menu_lateral, text="OPCIONES", bg="light yellow", font=("Arial", 12, "bold")).pack(pady=10)

        self.botones_menu = []  # <- almacena los botones

        opciones = [
            ("Agregar cuenta", self.ventana_agregar_cuenta),
            ("Ver cuentas", self.ventana_ver_cuentas),
            ("Agregar movimiento", self.ventana_agregar_movimiento),
            ("Ver movimientos", self.ventana_ver_movimientos),
            ("Agregar proyecto", self.ventana_agregar_proyecto),
            ("Ver proyectos", self.ventana_ver_proyectos),
        ]

        for texto, comando in opciones:
            btn = tk.Button(self.menu_lateral, text=texto, bg="light yellow", command=comando)
            btn.pack(fill="x", padx=10, pady=5)
            self.botones_menu.append(btn)

        # Botón de configuración
        btn_conf = tk.Button(self.menu_lateral, text="Configuración", bg="light yellow", command=None)
        btn_conf.pack(side="bottom", pady=10)
        self.botones_menu.append(btn_conf)

    

    def ventana_agregar_cuenta(self):
        self.TextoInicial.place_forget()

        # Si ya estaba empacado, no lo hagas otra vez
        self.zona_agregar_cuenta.place(x=201, y=45, width=250, height=300)

        for widget in self.zona_agregar_cuenta.winfo_children():
            widget.destroy()

        self.desactivar_botones()

        fondo_formulario = tk.Frame(self.zona_agregar_cuenta, bg="wheat2", bd=2, relief="solid")
        fondo_formulario.place(x= 0, y= 0, width=250, height=300)

        tk.Label(fondo_formulario, text="Ingrese los datos", bg="white", font=("Arial", 12)).pack(pady=(10, 15))

        tk.Label(fondo_formulario, text="Nombre de la cuenta", bg="white").pack(anchor="c", padx=20)
        entry_nombre = tk.Entry(fondo_formulario, width=30)
        entry_nombre.pack(padx=20, pady=(5, 15))

        tk.Label(fondo_formulario, text="Tipo de la cuenta", bg="white").pack(anchor="c", padx=20)
        entry_tipo = tk.Entry(fondo_formulario, width=30)
        entry_tipo.pack(padx=20, pady=(5, 15))

        tk.Label(fondo_formulario, text="Balance de la cuenta", bg="white").pack(anchor="c", padx=20)
        entry_balance = tk.Entry(fondo_formulario, width=30)
        entry_balance.pack(padx=20, pady=(5, 15))

        def guardar():
            nombre = entry_nombre.get()
            tipo = entry_tipo.get()
            balance_str = entry_balance.get()

            if not (nombre and tipo and balance_str):
                messagebox.showerror("ERROR", "Todos los campos son obligatorios")
                return
            
            try:
                balance = float(balance_str)
            except ValueError:
                messagebox.showerror("ERROR", "El saldo debe ser un numero")
                return

            agregar_cuenta(nombre,tipo,balance)
            messagebox.showinfo("EXITO", "Cuenta agregada correctamente")
            self.zona_agregar_cuenta.place_forget()
            self.activar_botones()
            self.animar_cerrar()

        def cerrar_formulario():
            self.zona_agregar_cuenta.place_forget()
            self.TextoInicial.place(relx=0.65 if self.menu_visible else 0.5, rely=0.2, anchor="center")
            self.activar_botones()

        boton_frame = tk.Frame(fondo_formulario, bg="wheat2")
        boton_frame.pack(pady=10)

        # 🔸 Botón Guardar
        tk.Button(boton_frame, text="Guardar", command=guardar).pack(side="left", padx=10)

        # 🔸 Botón Cancelar
        tk.Button(boton_frame, text="Cancelar", command=cerrar_formulario).pack(side="left", padx=10)
    
    def ventana_ver_cuentas(self):
        self.TextoInicial.place_forget()
        self.zona_ver_cuentas.place(x=205, y=0, width=489, height=495)
        for widget in self.zona_ver_cuentas.winfo_children():
            widget.destroy()

        self.desactivar_botones()

        info= tk.Label(self.zona_ver_cuentas, text="INFORMACIÓN DE CUENTAS",bg="light yellow", font=("Arial", 24, "bold"))
        info.pack(side="top", pady=50)

        fondo_tabla= tk.Frame(self.zona_ver_cuentas, bg="wheat2", bd=2, relief="solid")
        fondo_tabla.place(x=10, y=100, width=469, height=345)

        cuentas = obtener_cuentas()

        if not cuentas:
            tk.Label(fondo_tabla, text= "No hay cuentas registradas").pack(pady= 20)
        else:
            texto = tk.Text(fondo_tabla, width=469, height=345)
            texto.pack()


            texto.insert(tk.END, f"_________________________________________________________\n")
            texto.insert(tk.END, f"\n      Id    |    Nombre    |    Tipo    |    Balance    \n")
            texto.insert(tk.END, f"_________________________________________________________\n")
            for cuenta in cuentas:
                id, nombre, tipo, balance = cuenta
                texto.insert(tk.END, f"\n{id:>8}    |{nombre:^14}|{tipo:^12}|{f'${balance:.2f}':>11}    \n")
                texto.insert(tk.END, f"_________________________________________________________\n")

        def cerrar_tabla():
            self.zona_ver_cuentas.place_forget()
            self.TextoInicial.place(relx=0.65 if self.menu_visible else 0.5, rely=0.2, anchor="center")
            self.activar_botones()

        boton_frame = tk.Frame(self.zona_ver_cuentas, bg="light yellow")
        boton_frame.pack(side="bottom")


        tk.Button(boton_frame, text="SALIR", command=cerrar_tabla).pack(pady=10)


    def ventana_agregar_movimiento(self):
        pass

    def ventana_ver_movimientos(self):
        pass

    def ventana_agregar_proyecto(self):
        pass

    def ventana_ver_proyectos(self):
        pass



    def activar_botones(self):
        self.btn_menu.config(state="normal")
        for boton in self.botones_menu:
            boton.config(state="normal")

    def desactivar_botones(self):
        self.btn_menu.config(state="disabled")
        for boton in self.botones_menu:
            boton.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()  
    app = VentanaPrincipal(root)  
    root.mainloop()