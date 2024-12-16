from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtGui import QIcon
from datetime import datetime
from Class.Requerimento import Requerimento
from APP.Label.Label import get_status_description 
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
    
    table_data = [["Nome", "Tipo", "Qt Total", "Qt Alocada", "Qt Mínima", "Qt Pedido"]]
    for row in range(table_widget.rowCount()):
        row_data = [
            table_widget.item(row, 0).text(),
            table_widget.item(row, 1).text(),
            table_widget.item(row, 3).text(),
            table_widget.item(row, 4).text(),
            table_widget.item(row, 5).text(),
            table_widget.item(row, 6).text(),
        ]
        table_data.append(row_data)


    icon_paths = {
        "Medicamento": os.path.abspath("./icons/MaterialIcons/medicamento.png"),
        "Vacinas": os.path.abspath("./icons/MaterialIcons/vacina.png"),
        "Material Hospitalar": os.path.abspath("./icons/MaterialIcons/material_hospitalar.png"),
        "Outros": os.path.abspath("./icons/MaterialIcons/outro.png")
    }

    x_offset = 40
    y_offset = height - 100
    row_height = 22
    col_widths = [140, 105, 65, 75, 75, 75]
    icon_size = 14
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
            
            if col == 0 and row > 0:
                tipo_item = row_data[1]
                icon_path = icon_paths.get(tipo_item, None)
                if icon_path:
                    icon_x = x + 5
                    icon_y = y + (row_height - icon_size) / 2
                    c.drawImage(icon_path, icon_x, icon_y, width=icon_size, height=icon_size, mask='auto')
                    text_x = icon_x + icon_size + 5
                else:
                    text_x = x + 5
            else:
                text_x = x + 5
            
            text_y = y + 4
            c.drawString(text_x, text_y, cell_data)
        y_offset -= row_height

    c.save()




def GeneratePdfRequerimento(file_path: str, requerimento: Requerimento):
    width, height = A4
    c = canvas.Canvas(file_path, pagesize=A4)

    def draw_header():
        header = os.path.abspath("./icons/MedStock/Footer.png")
        c.drawImage(header, 90, height - 40, width=width-200, height=30)
        c.setLineWidth(1)
        c.line(60, height - 50, width - 60, height - 50)
        c.setFont("Helvetica-Bold", 16)

    def check_page_space(y_offset, required_space):
        if y_offset - required_space < 50:
            c.showPage()
            draw_header()
            return height - 80
        return y_offset

    draw_header()
    c.drawString(60, height - 80, f"REQ-{requerimento.requerimento_id}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, height - 110, "Detalhes do Requerimento")
    c.setFont("Helvetica", 10)
    y_offset = height - 130

    # Detalhes básicos
    details = [
        ("Setor", requerimento.setor_nome_localizacao or "Não especificado"),
        ("Nome do Solicitante", requerimento.nome_utilizador_pedido or "Desconhecido"),
        ("Data do Pedido", datetime.strptime(requerimento.data_pedido, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M') if requerimento.data_pedido else "------------"),
        ("Urgente", "Sim" if requerimento.urgente else "Não"),
    ]

    for label, value in details:
        y_offset = check_page_space(y_offset, 20)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y_offset, f"{label}:")
        label_width = c.stringWidth(f"{label}:", "Helvetica-Bold", 12)
        c.setFont("Helvetica", 10)
        c.drawString(60 + label_width + 5, y_offset, value)
        y_offset -= 20

    # Histórico
    if requerimento.historico:
        y_offset = check_page_space(y_offset, 30)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y_offset, "Histórico:")
        y_offset -= 20

        for hist in requerimento.historico:
            y_offset = check_page_space(y_offset, 40)
            match hist.requerimento_status:
                case 0:
                    text = f"           Pedido criado por {hist.user_responsavel} em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                    textcomentario= ""
                case 1:
                    if requerimento.status_anterior == 6:
                        text = f"           Requerimento enviado novamente para a lista de espera por {hist.user_responsavel } em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                        textcomentario= ""
                    else:
                        text = f"           Avaliado por {hist.user_responsavel} em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                        textcomentario= ""
                case 2:
                    text = f"           Pedido enviado para preparar por {hist.user_responsavel } em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                    textcomentario= ""
                case 3:
                    text = f"           Preparado por {hist.user_responsavel } em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                    textcomentario= ""
                case 4:
                    text = f"           Finalizado e Validado por {hist.user_responsavel} em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                    if hist.descricao:
                        descricao_limpa = hist.descricao.replace("Requerimento finalizado.", "").strip()
                        if descricao_limpa:
                            textcomentario = f"           Comentário: {descricao_limpa}"
                        else:
                            textcomentario = ""
                    else:
                        textcomentario = ""
                case 5:
                    text = f"           Recusado por {hist.user_responsavel } em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}." #Motivo: {hist.descricao or 'Não especificado'}"
                    textcomentario= ""
                case 6:
                    text = f"           Colocado em Stand By por {hist.user_responsavel } em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                    textcomentario= ""
                case 7:
                    text = f"           Cancelado por {hist.user_responsavel } em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                    textcomentario= ""
                case 8:
                    text = f"           Enviado por por {hist.user_responsavel } em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                    textcomentario= ""
                case 9:
                    text = f"           Colocado em Revalidação por {hist.user_responsavel } em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                    textcomentario= ""
                case 10:
                    text = f"           Retornou para a Lista de Espera por {hist.user_responsavel } em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                    textcomentario= ""
                case _:
                    text = f"           Estado desconhecido registrado por {hist.user_responsavel } em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}"
                    textcomentario= ""

            c.setFont("Helvetica", 10)
            c.drawString(60, y_offset, text)
            y_offset -= 20
            if(textcomentario!=""):
                c.setFont("Helvetica-Oblique", 10)
                c.drawString(60, y_offset, textcomentario)
                y_offset -= 20

    y_offset -= 10
    draw_status_label(c, 60, y_offset, requerimento.status_atual)
    y_offset -= 30


    icon_paths = {
        "Medicamento": os.path.abspath("./icons/MaterialIcons/medicamento.png"),
        "Vacinas": os.path.abspath("./icons/MaterialIcons/vacina.png"),
        "Material Hospitalar": os.path.abspath("./icons/MaterialIcons/material_hospitalar.png"),
        "Outros": os.path.abspath("./icons/MaterialIcons/outro.png")
    }

    table_data = [["Nome", "Tipo", "Quantidade"]]
    for item in requerimento.itens_pedidos:
        table_data.append([item.nome_item, item.tipo_item, str(item.quantidade)])

    x_offset = 60
    col_widths = [180, 150, 150]
    row_height = 20
    icon_size = 12
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
            
            if col == 1 and row > 0:
                tipo_item = cell_data
                icon_path = icon_paths.get(tipo_item)
                if icon_path:
                    icon_x = x + (col_widths[col] - icon_size) / 2
                    icon_y = y + (row_height - icon_size) / 2
                    c.drawImage(icon_path, icon_x, icon_y, width=icon_size, height=icon_size, mask='auto')
                    text_x = x + (col_widths[col] - icon_size) / 2 + icon_size + 10
                else:
                    text_x = x + col_widths[col] / 2 - c.stringWidth(cell_data, "Helvetica", 10) / 2
            else:
                text_x = x + col_widths[col] / 2 - c.stringWidth(cell_data, "Helvetica", 10) / 2
            
            text_y = y + row_height / 4
            c.drawString(text_x, text_y, cell_data)
        
        y_offset -= row_height
    c.save()




def draw_status_label(c, x, y, status):
    status_text, qcolor = get_status_description(status)
    
    rgb_color = (qcolor.red() / 255, qcolor.green() / 255, qcolor.blue() / 255)
    c.setFillColorRGB(*rgb_color)
    c.roundRect(x, y - 20, 250, 30, 10, fill=1, stroke=0)
    c.setFillColor("white")
    c.setFont("Helvetica-Bold", 16)
    text_width = c.stringWidth(status_text, "Helvetica-Bold", 16)
    text_x = x + (250 - text_width) / 2
    c.drawString(text_x, y - 5, status_text)