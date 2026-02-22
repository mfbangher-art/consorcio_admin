# pdf/generator.py
from fpdf import FPDF
from datetime import datetime
from models.owner import Owner
from models.income import Income
from models.expense import Expense

class PDFGenerator(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Consorcio – Reporte", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def generar_intimacion_pago(owner_id, file_path):
    """Genera un PDF de intimación de pago para un propietario."""
    owner = Owner.get_by_id(owner_id)
    if not owner:
        raise ValueError("Propietario no encontrado")

    pdf = PDFGenerator()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Intimación de Pago", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, f"Propietario: {owner[1]}", ln=True)
    pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(10)

    # Tabla de ingresos pendientes (ejemplo)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 10, "Concepto", 1)
    pdf.cell(40, 10, "Monto", 1)
    pdf.cell(40, 10, "Fecha", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    # En un caso real se filtrarían los ingresos pendientes
    incomes = Income.get_all()
    for inc in incomes:
        pdf.cell(60, 10, inc[2] or "N/A", 1)
        pdf.cell(40, 10, f"${inc[3]:,.2f}", 1)
        pdf.cell(40, 10, inc[4], 1)
        pdf.ln()

    pdf.output(file_path)
    return file_path

def generar_solicitud(file_path):
    """Genera un PDF con un formulario genérico de solicitud."""
    pdf = PDFGenerator()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Solicitud", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, "Nombre:", ln=True)
    pdf.cell(0, 10, "Dirección:", ln=True)
    pdf.cell(0, 10, "Teléfono:", ln=True)
    pdf.cell(0, 10, "Correo:", ln=True)
    pdf.ln(20)
    pdf.cell(0, 10, "Motivo de la solicitud:", ln=True)
    pdf.multi_cell(0, 10, "____________________________________________")
    pdf.output(file_path)
    return file_path

def generar_info_consignorio(file_path):
    """Genera un PDF con información corporativa del consorcio."""
    pdf = PDFGenerator()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Información del Consorcio", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, """
Nombre del Consorcio: Ejemplo Consorcio S.A.
Dirección: Calle Falsa 123, Ciudad.
Teléfono: 555-1234
Correo: contacto@consorcio.com
Representante Legal: Juan Pérez
    """)
    pdf.output(file_path)
    return file_path

