import flet as ft

def login_button_clicked(email_input, password_input):
    email = email_input.value
    password = password_input.value
    print(f"Login attempted with email: {email}, password: {password}")
    
def reset_password_button_clicked(e):
    print("Esqueci-me da Palavra-Passe")
    
    
def toggle_password_visibility(password_input, icon_button):
    password_input.password = not password_input.password
    icon_button.icon = ft.icons.VISIBILITY_OFF if password_input.password else ft.icons.VISIBILITY
    password_input.update()
    icon_button.update()