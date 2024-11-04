import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviarEmailRegistro(receiver_email, password):
    sender_email = os.getenv('EMAIL')
    password_email = os.getenv('PW')

    # Configuração da mensagem
    message = MIMEMultipart("alternative")
    message["Subject"] = "MedStock - Conta Criada com Sucesso"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = f"""\
    <html>
    <body>
    <div style="max-width: 600px; margin: 20px auto; padding: 20px; background: #ffffff; border: 1px solid #ddd; border-radius: 7px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; color: #333;">
        <div style="background: #89c379; color: #ffffff; padding: 10px; text-align: center; border-radius: 7px 7px 0 0;">
            <h2 style="margin: 0;">MedStock - Conta Criada com Sucesso</h2>
        </div>
        <div style="padding: 20px; text-align: left;">
            <p>Olá,</p>
            <p>A sua conta no MedStock foi criada com sucesso.</p>
            <p><strong>Sua Palavra-Passe:</strong> {password}</p>
            <p>Por segurança, recomendamos que você altere sua Palavra-Passe ao fazer o primeiro login. Para isso faça um pedido, no menu de Login, na parte inferior da página, onde existe um botão <em></strong>"Esqueci-me da Palavra-Passe"</strong></em>.</p>
            <p>Se você não solicitou essa conta, ignore este email.</p>
        </div>
        <div style="text-align: center; padding: 10px 0; color: #aaa; font-size: 12px;">
            <p>Obrigado,</p>
            <p>Equipe MedStock</p>
        </div>
    </div>
    </body>
    </html>
    """

    # Parte HTML
    part2 = MIMEText(html, "html")
    message.attach(part2)

    # Envio do e-mail
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password_email)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
        return True
    except Exception as e:
        return False

