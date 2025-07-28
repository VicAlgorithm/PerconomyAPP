import tkinter as tk
from tkinter import messagebox
from controlador.logica import *

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("PerconomyAPP - Economía Personal")
        self.root.geometry("400x300")

        tk.Label(root, text="Bienvenido a PerconomyApp", font=('Arial', 14)).pack(pady = 20)

        btn_agregar_cuenta = tk.Button(root, text = "Agregar Cuenta", command=self.ventana_agregar_cuenta)
        btn_agregar_cuenta.pack(pady = 10)

        btn_ver_cuentas = tk.Button(root, text = "Ver cuentas", command= self.ventana_ver_cuentas)
        btn_ver_cuentas.pack(pady=10)

    def ventana_agregar_cuenta(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Cuenta")
        ventana.geometry("300x250")
        
        tk.Label(ventana, text = "Nombre de la cuenta").pack()
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack()

        tk.Label(ventana, text = "Tipo de Cuenta").pack()
        entry_tipo = tk.Entry(ventana)
        entry_tipo.pack()

        tk.Label(ventana, text = "Balance Inicial").pack()
        entry_balance = tk.Entry(ventana)
        entry_balance.pack()

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
            ventana.destroy()

        tk.Button(ventana, text = "Guardar", command=guardar).pack(pady=10)

    def ventana_ver_cuentas(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Cuentas Registradas")
        ventana.geometry("700x300")
        ventana.minsize(700,300)

        cuentas = obtener_cuentas()

        if not cuentas:
            tk.Label(ventana, text = "No hay cuentas registradas.").pack(pady = 20)
            return

        texto = tk.Text(ventana, width=80, height=15)
        texto.pack(padx=10, pady= 10)

        for cuenta in cuentas:
            id, nombre, tipo, balance = cuenta
            texto.insert(tk.END, f"|ID: {id}|    |Nombre: {nombre:>10}|    |Tipo: {tipo:>10}|    |Balance: ${balance:>7.2f}|\n")
        texto.config(state="disabled")



if __name__ == "__main__":
    root = tk.Tk()  
    app = VentanaPrincipal(root)  