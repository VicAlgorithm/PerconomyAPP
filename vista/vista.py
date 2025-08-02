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


        self.contenedor = tk.Frame(self.root,  bg= "light yellow")
        self.contenedor.pack(fill="both", expand=True)


        self.menu_lateral = tk.Frame(self.contenedor, bg="DeepSkyBlue4", width=200)
        self.menu_visible = False 
        self.menu_lateral.lift()

        self.nomenu_lateral = tk.Frame(self.contenedor, bg="DeepSkyBlue4", width=45)
        self.nomenu_lateral.pack(side="left", fill="y")
        self.nomenu_visible = True
        self.nomenu_lateral.lift()


        self.icono_menu = tk.PhotoImage(file="a.png").subsample(30, 30)
        self.btn_menu = tk.Button(self.contenedor, image=self.icono_menu,  bg= "lightyellow2", command=self.toggle_menu)
        self.btn_menu.place(x=1, y=1)

        self.TextoInicial = tk.Label(self.contenedor, text="PerconomyAPP", bg="light yellow", font=("Arial", 24, "bold"))
        self.TextoInicial.place(relx=0.5, rely=0.2, anchor="center")

        self.zona_agregar = tk.Frame(self.contenedor, bg="light yellow")  
        self.zona_ver = tk.Frame(self.contenedor, bg="light yellow")  
        self.zonaver = False
        self.zonamovimientos = False




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

        self.botones_menu = [] 

        opciones = [
            ("Agregar cuenta", self.ventana_agregar_cuenta),
            ("Agregar movimiento", self.ventana_agregar_movimiento),
            ("Agregar proyecto", self.ventana_agregar_proyecto),
            ("Ver cuentas", self.ventana_ver_cuentas),
        ]

        for texto, comando in opciones:
            btn = tk.Button(self.menu_lateral, text=texto, bg="light yellow", command=comando)
            btn.pack(fill="x", padx=10, pady=5)
            self.botones_menu.append(btn)

       
        btn_conf = tk.Button(self.menu_lateral, text="Configuración", bg="light yellow", command=None)
        btn_conf.pack(side="bottom", pady=10)
        self.botones_menu.append(btn_conf)
    
    def activar_botones(self):
        self.btn_menu.config(state="normal")
        for boton in self.botones_menu:
            boton.config(state="normal")

    def desactivar_botones(self):
        self.btn_menu.config(state="disabled")
        for boton in self.botones_menu:
            boton.config(state="disabled")
    





    def ventana_agregar_cuenta(self):
        self.TextoInicial.place_forget()

        
        self.zona_agregar.place(x=201, y=45, width=250, height=300)

        for widget in self.zona_agregar.winfo_children():
            widget.destroy()

        self.desactivar_botones()

        fondo_formulario = tk.Frame(self.zona_agregar, bd=2, relief="solid")
        fondo_formulario.place(x= 0, y= 0, width=250, height=300)

        tk.Label(fondo_formulario, text="Ingrese los datos", font=("Arial", 17, "bold")).pack(pady=(10, 15))

        tk.Label(fondo_formulario, text="Nombre de la cuenta", font=("Arial", 10, "bold")).pack(anchor="c", padx=20)
        entry_nombre = tk.Entry(fondo_formulario, bg="light yellow", width=30)
        entry_nombre.pack(padx=20, pady=(5, 15))

        tk.Label(fondo_formulario, text="Tipo de la cuenta", font=("Arial", 10, "bold")).pack(anchor="c", padx=20)
        entry_tipo = tk.Entry(fondo_formulario, bg="light yellow", width=30)
        entry_tipo.pack(padx=20, pady=(5, 15))

        tk.Label(fondo_formulario, text="Balance de la cuenta", font=("Arial", 10, "bold")).pack(anchor="c", padx=20)
        entry_balance = tk.Entry(fondo_formulario, bg="light yellow", width=30)
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
            self.zona_agregar.place_forget()
            self.activar_botones()

            if self.zonaver == True:
                self.ventana_ver_cuentas()
            else:
                self.animar_cerrar()

        def cerrar_formulario():
            self.zona_agregar.place_forget()
            self.TextoInicial.place(relx=0.65 if self.menu_visible else 0.5, rely=0.2, anchor="center")
            self.activar_botones()

        boton_frame = tk.Frame(fondo_formulario)
        boton_frame.pack(pady=10)

        tk.Button(boton_frame, text="Guardar", bg="light yellow", command=guardar).pack(side="left", padx=10)

        tk.Button(boton_frame, text="Cancelar", bg="light yellow", command=cerrar_formulario).pack(side="left", padx=10)

    def ventana_agregar_movimiento(self):
        self.TextoInicial.place_forget()
        self.zona_agregar.place(x=201, y=45, width=498, height=300)

        for widget in self.zona_agregar.winfo_children():
            widget.destroy()

        self.desactivar_botones()

        fondo_formulario = tk.Frame(self.zona_agregar, bd=2, relief="solid", bg="white")
        fondo_formulario.place(x=0, y=0, width=498, height=300)

        tk.Label(fondo_formulario, text="Ingrese los datos", font=("Arial", 17, "bold"), bg="white").grid(
            row=0, column=0, columnspan=4, pady=(10, 25)
        )

        
        fondo_formulario.grid_columnconfigure(0, weight=1)
        fondo_formulario.grid_columnconfigure(1, weight=1)
        fondo_formulario.grid_columnconfigure(2, weight=1)
        fondo_formulario.grid_columnconfigure(3, weight=1)

        
        tk.Label(fondo_formulario, text="Fecha", font=("Arial", 10, "bold"), bg="white").grid(row=1, column=0, columnspan=2, sticky="w", padx=20)
        entry_fecha = tk.Entry(fondo_formulario, bg="light yellow", width=25)
        entry_fecha.grid(row=2, column=0, columnspan=2, sticky="w", padx=20)

        tk.Label(fondo_formulario, text="Tipo", font=("Arial", 10, "bold"), bg="white").grid(row=3, column=0, columnspan=2, sticky="w", padx=20)
        entry_tipo = tk.Entry(fondo_formulario, bg="light yellow", width=25)
        entry_tipo.grid(row=4, column=0, columnspan=2, sticky="w", padx=20)

        tk.Label(fondo_formulario, text="Categoria", font=("Arial", 10, "bold"), bg="white").grid(row=5, column=0, columnspan=2, sticky="w", padx=20)
        entry_categoria = tk.Entry(fondo_formulario, bg="light yellow", width=25)
        entry_categoria.grid(row=6, column=0, columnspan=2, sticky="w", padx=20)

        tk.Label(fondo_formulario, text="Descripción", font=("Arial", 10, "bold"), bg="white").grid(row=7, column=0, columnspan=2, sticky="w", padx=20)

        
        entry_descripcion = tk.Text(
            fondo_formulario,
            width=40,    
            height=4,   
            bg="light yellow",
            font=("Arial", 10),
            relief="solid",
            borderwidth=1
        )
        entry_descripcion.grid(row=8, column=0, columnspan=3, sticky="w", padx=20)

        
        tk.Label(fondo_formulario, text="Monto", font=("Arial", 10, "bold"), bg="white").grid(row=1, column=2, columnspan=2, sticky="w", padx=10)
        entry_monto = tk.Entry(fondo_formulario, bg="light yellow", width=25)
        entry_monto.grid(row=2, column=2, columnspan=2, sticky="w", padx=10)

        tk.Label(fondo_formulario, text="Cuenta_id", font=("Arial", 10, "bold"), bg="white").grid(row=3, column=2, columnspan=2, sticky="w", padx=10)
        entry_cuenta_id = tk.Entry(fondo_formulario, bg="light yellow", width=25)
        entry_cuenta_id.grid(row=4, column=2, columnspan=2, sticky="w", padx=10)

        tk.Label(fondo_formulario, text="Proyecto_id (Opcional)", font=("Arial", 10, "bold"), bg="white").grid(row=5, column=2, columnspan=2, sticky="w", padx=10)
        entry_proyecto_id = tk.Entry(fondo_formulario, bg="light yellow", width=25)
        entry_proyecto_id.grid(row=6, column=2, columnspan=2, sticky="w", padx=10)


        def guardar():
            fecha = entry_fecha.get()
            tipo = entry_tipo.get()
            categoria = entry_categoria.get()
            descripcion = descripcion = entry_descripcion.get("1.0", "end-1c")
            monto = entry_monto.get()
            cuenta_id = entry_cuenta_id.get()
            proyecto_id = entry_proyecto_id.get()

            if not (fecha and tipo and categoria and descripcion and monto and cuenta_id):
                messagebox.showerror("ERROR", "Favor de llenar campos obligatorios")
                return

            try:
                monto = float(monto)
                cuenta_id = int(cuenta_id)

                if proyecto_id:
                    proyecto_id = int(proyecto_id)
                else:
                    proyecto_id = None

            except ValueError:
                messagebox.showerror("ERROR", "El monto e id's deben ser numericos")
                return
        
            agregar_movimiento(fecha, tipo, categoria, descripcion, monto, cuenta_id, proyecto_id)

            messagebox.showinfo("EXITO", "Movimiento agregado correctamente")
            self.zona_agregar.place_forget()
            self.activar_botones()

            if self.zonaver == True:
                self.ventana_ver_cuentas()
            else:
                self.animar_cerrar()

        def cerrar_formulario():
            self.zona_agregar.place_forget()
            self.TextoInicial.place(relx=0.65 if self.menu_visible else 0.5, rely=0.2, anchor="center")
            self.activar_botones()
        
        boton_frame = tk.Frame(fondo_formulario, bg="white")
        boton_frame.grid(row=8, column=2, rowspan=2, sticky="n", padx=(85, 0), pady=(0, 5))



        tk.Button(boton_frame, text="Guardar", bg="light yellow", command=guardar)\
            .grid(row=0, column=1, pady=5)

        tk.Button(boton_frame, text="Cancelar", bg="light yellow", command=cerrar_formulario)\
            .grid(row=1, column=1, pady=5)
    
    def ventana_agregar_proyecto(self):
        pass

    def ventana_ver_cuentas(self):
        self.zonaver = True
        self.TextoInicial.place_forget()
        self.zona_ver.place(x=205, y=0, width=489, height=495)
        for widget in self.zona_ver.winfo_children():
            widget.destroy()

        

        info= tk.Label(self.zona_ver, text="INFORMACIÓN",bg="light yellow", font=("Arial", 24, "bold"))
        info.pack(side="top", pady=40)

        fondo_tabla= tk.Frame(self.zona_ver, bg="light yellow", bd=2, relief="solid")
        fondo_tabla.place(x=10, y=100, width=469, height=345)
        
        cuentas = obtener_cuentas()
        movimientos = obtener_movimientos()

        tabla_boton = tk.Frame(fondo_tabla, bg="light yellow")
        tabla_boton.pack(fill="x")

        def Cuentas():
            self.zonamovimientos = False
            for widget in boton_frame.winfo_children():
                widget.destroy()

            for widget in fondo_tabla.winfo_children():
                if widget != tabla_boton:
                    widget.destroy()

            botones_grame()
            if not cuentas:
                tk.Label(fondo_tabla, text= "No hay cuentas registradas", font=("Arial", 13, "bold")).pack(pady= 20)
                
            else:
                texto = tk.Text(
                fondo_tabla,
                width=56,          
                height=18,
                wrap="none",
                borderwidth=0,
                font=("Courier", 10),
                padx=6, pady=6,     
                bg="light yellow",         
                relief="flat",
                )
                texto.place(x=2, y=28) 

                

                texto.insert(tk.END, f"\n      Id    |    Nombre    |    Tipo    |    Balance    \n")
                texto.insert(tk.END, f"_________________________________________________________\n")
                for cuenta in cuentas:
                    id, nombre, tipo, balance = cuenta
                    texto.insert(tk.END, f"\n{id:>8}    |{nombre:^14}|{tipo:^12}|{f'${balance:.2f}':>11}    \n")
                    texto.insert(tk.END, f"_________________________________________________________\n")

        def Movimientos():
            self.zonamovimientos = True
            for widget in boton_frame.winfo_children():
                widget.destroy()

            for widget in fondo_tabla.winfo_children():
                if widget != tabla_boton:
                    widget.destroy()

            botones_grame()
            if not movimientos:
                tk.Label(fondo_tabla, text= "No hay movimientos registrados", font=("Arial", 13, "bold")).pack(pady= 20)
            else:
                texto = tk.Text(
                fondo_tabla,
                width=56,          
                height=18,
                wrap="none",
                borderwidth=0,
                font=("Courier", 10),
                padx=6, pady=6,     
                bg="light yellow",         
                relief="flat",
                )
                texto.place(x=2, y=28) 

                

                
                texto.tag_configure("azul", foreground="DeepSkyBlue4")

                
                texto.insert(tk.END, "\nId", )
                texto.insert(tk.END, "|", "azul")
                texto.insert(tk.END, "  Fecha   ")
                texto.insert(tk.END, "|", "azul")
                texto.insert(tk.END, "   Tipo   ")
                texto.insert(tk.END, "|", "azul")
                texto.insert(tk.END, " Categoria ")
                texto.insert(tk.END, "|", "azul")
                texto.insert(tk.END, "idC")
                texto.insert(tk.END, "|", "azul")
                texto.insert(tk.END, "idP")
                texto.insert(tk.END, "|", "azul")
                texto.insert(tk.END, " Monto  \n")

                # Línea divisoria
                texto.insert(tk.END, "_______________________________________________________\n", "azul")

                # Cuerpo de la tabla
                for movimiento in movimientos:
                    id, fecha, tipo, categoria, descripcion, monto, cuenta_id, proyecto_id = movimiento
                    proyecto_id = proyecto_id if proyecto_id is not None else ""
                    
                    try:
                        monto_float = float(monto)
                    except ValueError:
                        monto_float = 0.0

                    texto.insert(tk.END, f"\n{id:>2}")
                    texto.insert(tk.END, "|", "azul")
                    texto.insert(tk.END, f"{fecha:^10}")
                    texto.insert(tk.END, "|", "azul")
                    texto.insert(tk.END, f"{tipo:^10}")
                    texto.insert(tk.END, "|", "azul")
                    texto.insert(tk.END, f"{categoria:^11}")
                    texto.insert(tk.END, "|", "azul")
                    texto.insert(tk.END, f"{cuenta_id:^3}")
                    texto.insert(tk.END, "|", "azul")
                    texto.insert(tk.END, f"{proyecto_id:^3}")
                    texto.insert(tk.END, "|", "azul")
                    texto.insert(tk.END, "$", "azul")
                    texto.insert(tk.END, f"{monto_float:>8.2f}\n")

                    texto.insert(tk.END, "_______________________________________________________\n", "azul")




        tk.Button(tabla_boton, text="Cuentas", command=Cuentas).pack(side="left", fill="both", expand=True)
        tk.Button(tabla_boton, text="Movimientos", command=Movimientos).pack(side="left", fill="both", expand=True)
        tk.Button(tabla_boton, text="Proyectos", command=None).pack(side="left", fill="both", expand=True)
        tk.Button(tabla_boton, text="Deudas", command=None).pack(side="left", fill="both", expand=True)

        def info_movi():

            dic = {}
            for movimiento in movimientos:
                id, fecha, tipo, categoria, descripcion, monto, cuenta_id, proyecto_id = movimiento
                dic[id] = descripcion

            ventana_descripcion = tk.Toplevel()
            ventana_descripcion.title("Descripción")
            ventana_descripcion.geometry("400x300")

            tk.Label(ventana_descripcion, text="Ingrese la ID del movimiento:").pack(pady=10)
            entry_id = tk.Entry(ventana_descripcion)
            entry_id.pack(pady=5)

            texto = tk.Text(ventana_descripcion, height=10, wrap="word")
            texto.pack(pady=10, fill="both", expand=True)

            def mostrar_descripcion():
                try:
                    id_mov = int(entry_id.get())
                except ValueError:
                    texto.delete("1.0", tk.END)
                    texto.insert(tk.END, "La ID debe ser un número.")
                    return

                descripcion = dic.get(id_mov, "No se encontró descripción para esa ID.")
                texto.delete("1.0", tk.END)
                texto.insert(tk.END, descripcion)

            tk.Button(ventana_descripcion, text="Mostrar descripción", command=mostrar_descripcion).pack(pady=5)


            
            

        def cerrar_tabla():
            self.zona_ver.place_forget()
            self.TextoInicial.place(relx=0.65 if self.menu_visible else 0.5, rely=0.2, anchor="center")
            self.activar_botones()
            self.zonaver = False

        boton_frame = tk.Frame(self.zona_ver, bg="light yellow")
        boton_frame.pack(side="bottom")

        if self.zonaver == True:
            self.zona_agregar.lift()


        def botones_grame():
            tk.Button(boton_frame, text="SALIR", command=cerrar_tabla).pack(side="left", fill="both")
            if self.zonamovimientos ==True:
                a= tk.Button(boton_frame, text="Descripción", command=info_movi).pack(side="left", fill="both")






if __name__ == "__main__":
    root = tk.Tk()  
    app = VentanaPrincipal(root)  
    root.mainloop()