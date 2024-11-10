from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PyQt5.QtWidgets import QTableWidget
import os

def GeneratePdfItens(self, table_widget: QTableWidget, file_path: str):
    width, height = A4
    c = canvas.Canvas(file_path, pagesize=A4)
    
    def draw_header():
        header = os.path.abspath("./icons/MedStock/Footer.png")
        c.drawImage(header, 90, height - 40, width=width-200, height=30)
        c.setLineWidth(1)
        c.line(60, height - 50, width - 60, height - 50)
        c.setFont("Helvetica-Bold", 16)

    draw_header()
    c.drawString(60, height - 80, "Relatório de Itens Disponíveis")
    table_data = [["Nome", "Tipo", "Código", "Quantidade"]]
    for row in range(table_widget.rowCount()):
        row_data = [
            table_widget.item(row, 0).text(),
            table_widget.item(row, 1).text(),
            table_widget.item(row, 2).text(),
            table_widget.item(row, 3).text(),
        ]
        table_data.append(row_data)

    x_offset = 60
    y_offset = height - 100
    row_height = 20
    col_widths = [100, 130, 140, 110]
    
    min_y_offset = 50

    for row, row_data in enumerate(table_data):
        if y_offset - row_height < min_y_offset:
            c.showPage()
            draw_header()
            y_offset = height - 100  

        for col, cell_data in enumerate(row_data):
            x = x_offset + sum(col_widths[:col])
            y = y_offset - row_height
            
            if row == 0:
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(colors.whitesmoke)
                c.rect(x, y, col_widths[col], row_height, fill=1, stroke=0)  
                c.setFillColor(colors.black)
            else:
                c.setFont("Helvetica", 10)
                c.setFillColor(colors.black)
            
            c.setStrokeColor(colors.lightgrey)
            c.line(x_offset, y, x_offset + sum(col_widths), y)
            
            text_x = x + col_widths[col] / 2 - c.stringWidth(cell_data, "Helvetica", 10) / 2
            text_y = y + row_height / 4
            c.drawString(text_x, text_y, cell_data)
        
        y_offset -= row_height

    c.save()
