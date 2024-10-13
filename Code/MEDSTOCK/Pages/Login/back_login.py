
def login_button_clicked(email_input, password_input):
    email = email_input.value
    password = password_input.value
    print(f"Login attempted with email: {email}, password: {password}")
    
def reset_password_button_clicked(e):
    print("Esqueci-me da Palavra-Passe")
    
def register_button_clicked(e):
    print("Registar")