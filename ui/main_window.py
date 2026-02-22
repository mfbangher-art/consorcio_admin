# ui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from models.owner import Owner
from models.category import Category
from models.income import Income
from models.expense import Expense
from pdf.generator import (
    generar_intimacion_pago,
    generar_solicitud,
    generar_info_consignorio
)

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Consorcio – Gestión")
        self.root.geometry("900x600")

        # Barra de menús
        self._crear_menus()

        # Pestañas
        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill="both")

        self._crear_tablas()
        self._cargar_datos()

    # ---------- Menús ----------
    def _crear_menus(self):
        menubar = tk.Menu(self.root)

        # Menú de Propietarios
        propietario_menu = tk.Menu(menubar, tearoff=0)
        propietario_menu.add_command(label="Nuevo", command=self._agregar_owner)
        propietario_menu.add_command(label="Ver todos", command=self._mostrar_owners)
        menubar.add_cascade(label="Propietarios", menu=propietario_menu)

        # Menú de Rubros
        rubro_menu = tk.Menu(menubar, tearoff=0)
        rubro_menu.add_command(label="Nuevo", command=self._agregar_category)
        rubro_menu.add_command(label="Ver todos", command=self._mostrar_categories)
        menubar.add_cascade(label="Rubros", menu=rubro_menu)

        # Menú de Ingresos
        ingreso_menu = tk.Menu(menubar, tearoff=0)
        ingreso_menu.add_command(label="Nuevo", command=self._agregar_income)
        ingreso_menu.add_command(label="Ver todos", command=self._mostrar_incomes)
        menubar.add_cascade(label="Ingresos", menu=ingreso_menu)

        # Menú de Egresos
        egreso_menu = tk.Menu(menubar, tearoff=0)
        egreso_menu.add_command(label="Nuevo", command=self._agregar_expense)
        egreso_menu.add_command(label="Ver todos", command=self._mostrar_expenses)
        menubar.add_cascade(label="Egresos", menu=egreso_menu)

        # Menú de PDF
        pdf_menu = tk.Menu(menubar, tearoff=0)
        pdf_menu.add_command(label="Intimación de Pago", command=self._pdf_intimacion)
        pdf_menu.add_command(label="Solicitud", command=self._pdf_solicitud)
        pdf_menu.add_command(label="Info Consorcio", command=self._pdf_info)
        menubar.add_cascade(label="PDF", menu=pdf_menu)

        self.root.config(menu=menubar)

    # ---------- Pestañas ----------
    def _crear_tablas(self):
        # Pestaña de Propietarios
        self.owner_frame = ttk.Frame(self.tab_control)
        self.tab_control.add(self.owner_frame, text="Propietarios")
        self._crear_owner_tab()

        # Pestaña de Rubros
        self.category_frame = ttk.Frame(self.tab_control)
        self.tab_control.add(self.category_frame, text="Rubros")
        self._crear_category_tab()

        # Pestaña de Ingresos
        self.income_frame = ttk.Frame(self.tab_control)
        self.tab_control.add(self.income_frame, text="Ingresos")
        self._crear_income_tab()

        # Pestaña de Egresos
        self.expense_frame = ttk.Frame(self.tab_control)
        self.tab_control.add(self.expense_frame, text="Egresos")
        self._crear_expense_tab()

    # ---------- Propietarios ----------
    def _crear_owner_tab(self):
        # Campos de entrada
        ttk.Label(self.owner_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.owner_name_var = tk.StringVar()
        ttk.Entry(self.owner_frame, textvariable=self.owner_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.owner_frame, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.owner_phone_var = tk.StringVar()
        ttk.Entry(self.owner_frame, textvariable=self.owner_phone_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.owner_frame, text="Correo:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.owner_email_var = tk.StringVar()
        ttk.Entry(self.owner_frame, textvariable=self.owner_email_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.owner_frame, text="Agregar", command=self._guardar_owner).grid(row=3, column=0, columnspan=2, pady=10)

        # Lista de propietarios
        self.owner_list = ttk.Treeview(self.owner_frame, columns=("ID", "Nombre", "Tel", "Email"), show="headings")
        for col in ("ID", "Nombre", "Tel", "Email"):
            self.owner_list.heading(col, text=col)
            self.owner_list.column(col, width=100)
        self.owner_list.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=10)

        self.owner_frame.rowconfigure(4, weight=1)
        self.owner_frame.columnconfigure(1, weight=1)

    def _guardar_owner(self):
        name = self.owner_name_var.get()
        if not name:
            messagebox.showwarning("Datos incompletos", "El nombre es obligatorio.")
            return
        Owner.create(name, self.owner_phone_var.get(), self.owner_email_var.get())
        self._mostrar_owners()
        self.owner_name_var.set("")
        self.owner_phone_var.set("")
        self.owner_email_var.set("")

    def _mostrar_owners(self):
        for item in self.owner_list.get_children():
            self.owner_list.delete(item)
        for row in Owner.get_all():
            self.owner_list.insert("", "end", values=row)

    # ---------- Rubros ----------
    def _crear_category_tab(self):
        ttk.Label(self.category_frame, text="Nombre del rubro:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.category_name_var = tk.StringVar()
        ttk.Entry(self.category_frame, textvariable=self.category_name_var).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.category_frame, text="Agregar", command=self._guardar_category).grid(row=1, column=0, columnspan=2, pady=10)

        self.category_list = ttk.Treeview(self.category_frame, columns=("ID", "Nombre"), show="headings")
        for col in ("ID", "Nombre"):
            self.category_list.heading(col, text=col)
            self.category_list.column(col, width=150)
        self.category_list.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

        self.category_frame.rowconfigure(2, weight=1)
        self.category_frame.columnconfigure(1, weight=1)

    def _guardar_category(self):
        name = self.category_name_var.get()
        if not name:
            messagebox.showwarning("Datos incompletos", "El nombre del rubro es obligatorio.")
            return
        Category.create(name)
        self._mostrar_categories()
        self.category_name_var.set("")

    def _mostrar_categories(self):
        for item in self.category_list.get_children():
            self.category_list.delete(item)
        for row in Category.get_all():
            self.category_list.insert("", "end", values=row)

    # ---------- Ingresos ----------
    def _crear_income_tab(self):
        ttk.Label(self.income_frame, text="Propietario:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.income_owner_var = tk.StringVar()
        ttk.Combobox(self.income_frame, textvariable=self.income_owner_var, state="readonly").grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.income_frame, text="Rubros:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.income_category_var = tk.StringVar()
        ttk.Combobox(self.income_frame, textvariable=self.income_category_var, state="readonly").grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.income_frame, text="Monto:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.income_amount_var = tk.DoubleVar()
        ttk.Entry(self.income_frame, textvariable=self.income_amount_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.income_frame, text="Fecha (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.income_date_var = tk.StringVar()
        ttk.Entry(self.income_frame, textvariable=self.income_date_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.income_frame, text="Descripción:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.income_desc_var = tk.StringVar()
        ttk.Entry(self.income_frame, textvariable=self.income_desc_var).grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(self.income_frame, text="Agregar", command=self._guardar_income).grid(row=5, column=0, columnspan=2, pady=10)

        self.income_list = ttk.Treeview(self.income_frame, columns=("ID", "Propietario", "Rubros", "Monto", "Fecha", "Descripción"), show="headings")
        for col in ("ID", "Propietario", "Rubros", "Monto", "Fecha", "Descripción"):
            self.income_list.heading(col, text=col)
            self.income_list.column(col, width=120)
        self.income_list.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

        self.income_frame.rowconfigure(6, weight=1)
        self.income_frame.columnconfigure(1, weight=1)

    def _guardar_income(self):
        owner = self.income_owner_var.get()
        rubro = self.income_category_var.get()
        monto = self.income_amount_var.get()
        fecha = self.income_date_var.get()
        if not all([owner, rubro, monto, fecha]):
            messagebox.showwarning("Datos incompletos", "Todos los campos son obligatorios.")
            return
        # Obtener ID de propietario y rubro
        owner_id = next((row[0] for row in Owner.get_all() if row[1] == owner), None)
        category_id = next((row[0] for row in Category.get_all() if row[1] == rubro), None)
        if owner_id is None or category_id is None:
            messagebox.showerror("Error", "Propietario o rubro no encontrado.")
            return
        Income.create(owner_id, category_id, monto, fecha, self.income_desc_var.get())
        self._mostrar_incomes()
        # Limpiar campos
        self.income_owner_var.set("")
        self.income_category_var.set("")
        self.income_amount_var.set(0.0)
        self.income_date_var.set("")
        self.income_desc_var.set("")

    def _mostrar_incomes(self):
        for item in self.income_list.get_children():
            self.income_list.delete(item)
        for row in Income.get_all():
            self.income_list.insert("", "end", values=row)

    # ---------- Egresos ----------
    def _crear_expense_tab(self):
        # Similar a ingresos, pero con egresos
        ttk.Label(self.expense_frame, text="Propietario:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.expense_owner_var = tk.StringVar()
        ttk.Combobox(self.expense_frame, textvariable=self.expense_owner_var, state="readonly").grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.expense_frame, text="Rubros:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.expense_category_var = tk.StringVar()
        ttk.Combobox(self.expense_frame, textvariable=self.expense_category_var, state="readonly").grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.expense_frame, text="Monto:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.expense_amount_var = tk.DoubleVar()
        ttk.Entry(self.expense_frame, textvariable=self.expense_amount_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.expense_frame, text="Fecha (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.expense_date_var = tk.StringVar()
        ttk.Entry(self.expense_frame, textvariable=self.expense_date_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.expense_frame, text="Descripción:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.expense_desc_var = tk.StringVar()
        ttk.Entry(self.expense_frame, textvariable=self.expense_desc_var).grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(self.expense_frame, text="Agregar", command=self._guardar_expense).grid(row=5, column=0, columnspan=2, pady=10)

        self.expense_list = ttk.Treeview(self.expense_frame, columns=("ID", "Propietario", "Rubros", "Monto", "Fecha", "Descripción"), show="headings")
        for col in ("ID", "Propietario", "Rubros", "Monto", "Fecha", "Descripción"):
            self.expense_list.heading(col, text=col)
            self.expense_list.column(col, width=120)
        self.expense_list.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

        self.expense_frame.rowconfigure(6, weight=1)
        self.expense_frame.columnconfigure(1, weight=1)

    def _guardar_expense(self):
        owner = self.expense_owner_var.get()
        rubro = self.expense_category_var.get()
        monto = self.expense_amount_var.get()
        fecha = self.expense_date_var.get()
        if not all([owner, rubro, monto, fecha]):
            messagebox.showwarning("Datos incompletos", "Todos los campos son obligatorios.")
            return
        owner_id = next((row[0] for row in Owner.get_all() if row[1] == owner), None)
        category_id = next((row[0] for row in Category.get_all() if row[1] == rubro), None)
        if owner_id is None or category_id is None:
            messagebox.showerror("Error", "Propietario o rubro no encontrado.")
            return
        Expense.create(owner_id, category_id, monto, fecha, self.expense_desc_var.get())
        self._mostrar_expenses()
        self.expense_owner_var.set("")
        self.expense_category_var.set("")
        self.expense_amount_var.set(0.0)
        self.expense_date_var.set("")
        self.expense_desc_var.set("")

    def _mostrar_expenses(self):
        for item in self.expense_list.get_children():
            self.expense_list.delete(item)
        for row in Expense.get_all():
            self.expense_list.insert("", "end", values=row)

    # ---------- Cargar datos en combos ----------
    def _cargar_datos(self):
        # Propietarios en comboboxes
        owners = Owner.get_all()
        owner_names = [row[1] for row in owners]
        self.income_owner_var.set("")
        self.expense_owner_var.set("")
        self.income_owner_var.set(owner_names[0] if owner_names else "")
        self.expense_owner_var.set(owner_names[0] if owner_names else "")

        # Rubros en comboboxes
        categories = Category.get_all()
        category_names = [row[1] for row in categories]
        self.income_category_var.set("")
        self.expense_category_var.set("")
        self.income_category_var.set(category_names[0] if category_names else "")
        self.expense_category_var.set(category_names[0] if category_names else "")

    # ---------- PDF ----------
    def _pdf_intimacion(self):
        owner = self.owner_list.focus()
        if not owner:
            messagebox.showwarning("Seleccionar propietario", "Seleccione un propietario en la lista.")
            return
        owner_id = self.owner_list.item(owner)['values'][0]
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        generar_intimacion_pago(file_path, owner_id)

    def _pdf_solicitud(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        generar_solicitud(file_path)

    def _pdf_info(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        generar_info_consignorio(file_path)

# ---------- Ejecutar ----------
if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

