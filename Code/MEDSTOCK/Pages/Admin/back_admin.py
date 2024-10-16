import flet as ft


# Função de clique do botão de registro
def handle_register(page, nome_input, email_input, sexo_input, dia_input, mes_input, ano_input, role_input):
    data_nascimento = build_data_nascimento(dia_input, mes_input, ano_input)
    register_button_clicked(page, nome_input, email_input, sexo_input, data_nascimento, role_input)

# Função para construir a data de nascimento a partir dos dropdowns
def build_data_nascimento(dia_input, mes_input, ano_input):
    dia = dia_input.value
    mes = mes_input.value
    ano = ano_input.value
    
    if dia and mes and ano:
        return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
    return None

def close_dialog(page, dialog):
    if dialog in page.overlay:
        dialog.open = False  # Fecha o diálogo
        page.overlay.remove(dialog)  # Remove o diálogo do overlay
        page.update()

# Função que lida com o clique do botão de registro
def register_button_clicked(page, nome_input, email_input, sexo_input, data_nascimento_input, role_input):
    from Pages import show_overlay
    nome = nome_input.value
    email = email_input.value
    sexo = sexo_input.value
    data_nascimento = data_nascimento_input
    role_id = role_input.value
    
    if not all([nome, email, sexo, data_nascimento, role_id]):
        show_overlay(page, "Preencha todos os campos",alert_type="warning")
        return
    
    page.update()

