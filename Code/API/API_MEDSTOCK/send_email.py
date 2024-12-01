import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviarEmailRegistro(receiver_email:str, password:str):
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

def enviarEmailRequerimentoAceito(receiver_email:str, requerimento_id:int, itens_pedidos:list, nome_utilizador_confirmacao:str, data_confirmacao:str):
    
    sender_email = os.getenv('EMAIL')
    password_email = os.getenv('PW')

    # Configuração da mensagem
    message = MIMEMultipart("alternative")
    message["Subject"] = f"MedStock - Requerimento #{requerimento_id} Aceite"
    message["From"] = sender_email
    message["To"] = receiver_email

    if itens_pedidos is not None:
        itens_html = "".join(
            f"<li>{item['nome_item']} - Quantidade: {item['quantidade']}</li>"
            for item in itens_pedidos
        )
    else:
        itens_html = ""


    html = f"""\
    <html>
    <body>
    <div style="max-width: 600px; margin: 20px auto; padding: 20px; background: #ffffff; border: 1px solid #ddd; border-radius: 7px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; color: #333;">
        <div style="background: #89c379; color: #ffffff; padding: 10px; text-align: center; border-radius: 7px 7px 0 0;">
            <h2 style="margin: 0;">MedStock - Requerimento Aceite</h2>
        </div>
        <div style="padding: 20px; text-align: left;">
            <p>Olá,</p>
            <p>O requerimento <strong>REQ-{requerimento_id}</strong></p> foi aceite e está na lista de espera da farmácia para ser preparado.</p>
            <p>Aprovação realizada por: <strong>{nome_utilizador_confirmacao}</strong></p>
            <p>Data de Aprovação: <strong>{data_confirmacao.strftime('%d/%m/%Y %H:%M:%S')}</strong></p>
            <h3>Itens Solicitados:</h3>
            <ul>
                {itens_html}
            </ul>
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
        return True
    except Exception as e:
        return False



def enviarEmailRequerimentoRecusado(receiver_email: str, requerimento_id: int, itens_pedidos: list, nome_utilizador_confirmacao: str, data_confirmacao: str):
    sender_email = os.getenv('EMAIL')
    password_email = os.getenv('PW')

    # Configuração da mensagem
    message = MIMEMultipart("alternative")
    message["Subject"] = f"MedStock - Requerimento #{requerimento_id} Recusado"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Conteúdo HTML
    if itens_pedidos is not None:
        itens_html = "".join(
            f"<li>{item['nome_item']} - Quantidade: {item['quantidade']}</li>"
            for item in itens_pedidos
        )
    else:
        itens_html = ""

    html = f"""\
    <html>
    <body>
    <div style="max-width: 600px; margin: 20px auto; padding: 20px; background: #ffffff; border: 1px solid #ddd; border-radius: 7px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; color: #333;">
        <div style="background: #d9534f; color: #ffffff; padding: 10px; text-align: center; border-radius: 7px 7px 0 0;">
            <h2 style="margin: 0;">MedStock - Requerimento Recusado</h2>
        </div>
        <div style="padding: 20px; text-align: left;">
            <p>Prezado(a),</p>
            <p>Infelizmente, o requerimento <strong>REQ-{requerimento_id}</strong> foi recusado.</p>
            <p>Decisão realizada por: <strong>{nome_utilizador_confirmacao}</strong></p>
            <p>Data da decisão: <strong>{data_confirmacao.strftime('%d/%m/%Y %H:%M:%S')}</strong></p>
            <p>Abaixo está a lista dos itens solicitados no requerimento:</p>
            <ul>
                {itens_html}
            </ul>
            <p>Caso precise de assistência, não hesite em entrar em contato com o setor responsável.</p>
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
        return True
    except Exception as e:
        return False


