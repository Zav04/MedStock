import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


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
            <p>Prezado(a),</p>
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


def enviarEmailRequerimentoCriado(nome_utilizador_pedido:str,receiver_email:str, requerimento_id:int, itens_pedidos:list):
    
    sender_email = os.getenv('EMAIL')
    password_email = os.getenv('PW')

    # Configuração da mensagem
    message = MIMEMultipart("alternative")
    message["Subject"] = f"MedStock - Requerimento #{requerimento_id} Aceite"
    message["From"] = sender_email
    message["To"] = receiver_email

    if itens_pedidos is not None:
        itens_html = "".join(
            f"<li>{item['nome_consumivel']} - Quantidade: {item['quantidade']}</li>"
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
            <p>Prezado(a) {nome_utilizador_pedido},</p>
            <p>O requerimento <strong>REQ-{requerimento_id}</strong> foi criado, fique a espera pela aprovação da gestor responsável.</p>
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



def enviarEmailRequerimentoAceito(nome_utilizador_pedido:str,receiver_email:str, 
                                requerimento_id:int, itens_pedidos:list, user_responsavel:str, 
                                data_modificacao:str):
    
    sender_email = os.getenv('EMAIL')
    password_email = os.getenv('PW')

    # Configuração da mensagem
    message = MIMEMultipart("alternative")
    message["Subject"] = f"MedStock - Requerimento #{requerimento_id} Aceite"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    
    data_modificacao_datetime = datetime.strptime(data_modificacao, "%Y-%m-%dT%H:%M:%S")
    data_formatada = data_modificacao_datetime.strftime('%d/%m/%Y %H:%M:%S')

    if itens_pedidos is not None:
        itens_html = "".join(
            f"<li>{item['nome_consumivel']} - Quantidade: {item['quantidade']}</li>"
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
            <p>Prezado(a) {nome_utilizador_pedido},</p>
            <p>O requerimento <strong>REQ-{requerimento_id}</strong> foi aceite e está na lista de espera da farmácia para ser preparado.</p>
            <p>Aprovação realizada por: <strong>{user_responsavel}</strong></p>
            <p>Data de Aprovação: <strong>{data_formatada}</strong></p>
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



def enviarEmailRequerimentoRecusado(nome_utilizador_pedido:str,receiver_email: str, requerimento_id: int, 
                                    itens_pedidos: list, user_responsavel:str, data_modificacao:str):
    sender_email = os.getenv('EMAIL')
    password_email = os.getenv('PW')

    # Configuração da mensagem
    message = MIMEMultipart("alternative")
    message["Subject"] = f"MedStock - Requerimento #{requerimento_id} Recusado"
    message["From"] = sender_email
    message["To"] = receiver_email

    data_modificacao_datetime = datetime.strptime(data_modificacao, "%Y-%m-%dT%H:%M:%S")
    data_formatada = data_modificacao_datetime.strftime('%d/%m/%Y %H:%M:%S')

    # Conteúdo HTML
    if itens_pedidos is not None:
        itens_html = "".join(
            f"<li>{item['nome_consumivel']} - Quantidade: {item['quantidade']}</li>"
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
            <p>Prezado(a) {nome_utilizador_pedido},</p>
            <p>Infelizmente, o requerimento <strong>REQ-{requerimento_id}</strong> foi <strong>Recusado</strong>.</p>
            <p>Decisão realizada por: <strong>{user_responsavel}</strong></p>
            <p>Data da decisão: <strong>{data_formatada}</strong></p>
            <p>Abaixo está a lista dos itens solicitados no requerimento:</p>
            <ul>
                {itens_html}
            </ul>
            <p>Caso precise de assistência, não hesite em entrar em contato com o gestor responsável.</p>
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



def enviarEmailRequerimentoStandBy(nome_utilizador_pedido:str,receiver_email: str, requerimento_id: int, itens_pedidos: list):
    sender_email = os.getenv('EMAIL')
    password_email = os.getenv('PW')

    message = MIMEMultipart("alternative")
    message["Subject"] = f"MedStock - Requerimento #{requerimento_id} em Stand-By"
    message["From"] = sender_email
    message["To"] = receiver_email

    if itens_pedidos is not None:
        itens_html = "".join(
            f"<li>{item['nome_consumivel']} - Quantidade: {item['quantidade']}</li>"
            for item in itens_pedidos
        )
    else:
        itens_html = ""

    html = f"""\
    <html>
    <body>
    <div style="max-width: 600px; margin: 20px auto; padding: 20px; background: #ffffff; border: 1px solid #ddd; border-radius: 7px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; color: #333;">
        <div style="background: #f0ad4e; color: #ffffff; padding: 10px; text-align: center; border-radius: 7px 7px 0 0;">
            <h2 style="margin: 0;">MedStock - Requerimento em Stand-By</h2>
        </div>
        <div style="padding: 20px; text-align: left;">
            <p>Prezado(a) {nome_utilizador_pedido},</p>
            <p>O requerimento <strong>REQ-{requerimento_id}</strong> foi colocado em <strong>Stand-By</strong></p>
            <h3>Itens do Requerimento:</h3>
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

    part2 = MIMEText(html, "html")
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password_email)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        return False


def enviarEmailRequerimentoListaEspera(nome_utilizador_pedido:str,receiver_email: str, requerimento_id: int, itens_pedidos: list):
    sender_email = os.getenv('EMAIL')
    password_email = os.getenv('PW')

    message = MIMEMultipart("alternative")
    message["Subject"] = f"MedStock - Requerimento #{requerimento_id} Retornado à Lista de Espera"
    message["From"] = sender_email
    message["To"] = receiver_email

    if itens_pedidos is not None:
        itens_html = "".join(
            f"<li>{item['nome_consumivel']} - Quantidade: {item['quantidade']}</li>"
            for item in itens_pedidos
        )
    else:
        itens_html = ""

    html = f"""\
    <html>
    <body>
    <div style="max-width: 600px; margin: 20px auto; padding: 20px; background: #ffffff; border: 1px solid #ddd; border-radius: 7px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; color: #333;">
        <div style="background: #5bc0de; color: #ffffff; padding: 10px; text-align: center; border-radius: 7px 7px 0 0;">
            <h2 style="margin: 0;">MedStock - Requerimento Retornado à Lista de Espera</h2>
        </div>
        <div style="padding: 20px; text-align: left;">
            <p>Prezado(a) {nome_utilizador_pedido},</p>
            <p>O requerimento <strong>REQ-{requerimento_id}</strong> retornou à lista de espera da farmácia.</p>
            <h3>Itens do Requerimento:</h3>
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

    part2 = MIMEText(html, "html")
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password_email)
            server.sendmail(sender_email, message["To"], message.as_string())
        return True
    except Exception as e:
        return False



def enviarEmailRequerimentoPreparacao(nome_utilizador_pedido:str,receiver_email: str, requerimento_id: int, itens_pedidos: list):
    sender_email = os.getenv('EMAIL')
    password_email = os.getenv('PW')

    message = MIMEMultipart("alternative")
    message["Subject"] = f"MedStock - Requerimento #{requerimento_id} em Preparação"
    message["From"] = sender_email
    message["To"] = receiver_email

    if itens_pedidos is not None:
        itens_html = "".join(
            f"<li>{item['nome_consumivel']} - Quantidade: {item['quantidade']}</li>"
            for item in itens_pedidos
        )
    else:
        itens_html = ""

    html = f"""\
    <html>
    <body>
    <div style="max-width: 600px; margin: 20px auto; padding: 20px; background: #ffffff; border: 1px solid #ddd; border-radius: 7px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; color: #333;">
        <div style="background: #f0ad4e; color: #ffffff; padding: 10px; text-align: center; border-radius: 7px 7px 0 0;">
            <h2 style="margin: 0;">MedStock - Requerimento em Preparação</h2>
        </div>
        <div style="padding: 20px; text-align: left;">
            <p>Prezado(a) {nome_utilizador_pedido},</p>
            <p>O requerimento <strong>REQ-{requerimento_id}</strong> está atualmente em preparação pela farmácia.</p>
            <h3>Itens do Requerimento:</h3>
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

    part2 = MIMEText(html, "html")
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password_email)
            server.sendmail(sender_email, message["To"], message.as_string())
        return True
    except Exception as e:
        return False


def enviarEmailRequerimentoProntoEntrega(nome_utilizador_pedido:str,receiver_email: str, requerimento_id: int, 
                                        itens_pedidos: list, user_responsavel: str, data_modificacao:str):
    sender_email = os.getenv('EMAIL')
    password_email = os.getenv('PW')

    message = MIMEMultipart("alternative")
    message["Subject"] = f"MedStock - Requerimento #{requerimento_id} Pronto para Entrega"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    data_modificacao_datetime = datetime.strptime(data_modificacao, "%Y-%m-%dT%H:%M:%S")
    data_formatada = data_modificacao_datetime.strftime('%d/%m/%Y %H:%M:%S')

    if itens_pedidos is not None:
        itens_html = "".join(
            f"<li>{item['nome_consumivel']} - Quantidade: {item['quantidade']}</li>"
            for item in itens_pedidos
        )
    else:
        itens_html = ""

    html = f"""\
    <html>
    <body>
    <div style="max-width: 600px; margin: 20px auto; padding: 20px; background: #ffffff; border: 1px solid #ddd; border-radius: 7px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; color: #333;">
        <div style="background: #5cb85c; color: #ffffff; padding: 10px; text-align: center; border-radius: 7px 7px 0 0;">
            <h2 style="margin: 0;">MedStock - Requerimento Pronto para Entrega</h2>
        </div>
        <div style="padding: 20px; text-align: left;">
            <p>Prezado(a) {nome_utilizador_pedido},</p>
            <p>O requerimento <strong>REQ-{requerimento_id}</strong> está pronto para entrega e será enviado brevemente.</p>
            <p>Pedido realizado por: <strong>{user_responsavel}</strong> em <strong>{data_formatada}</strong>.</p>
            <h3>Itens do Requerimento:</h3>
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

    part2 = MIMEText(html, "html")
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password_email)
            server.sendmail(sender_email, message["To"], message.as_string())
        return True
    except Exception as e:
        return False

def enviarEmailRequerimentoEntregue(
    nome_utilizador_pedido:str,
    receiver_email: str,
    requerimento_id: int,
    itens_pedidos: list,
    user_responsavel:str, 
    data_modificacao:str
):
    sender_email = os.getenv('EMAIL')
    password_email = os.getenv('PW')

    message = MIMEMultipart("alternative")
    message["Subject"] = f"MedStock - Requerimento #{requerimento_id} Entregue"
    message["From"] = sender_email
    message["To"] = receiver_email

    data_modificacao_datetime = datetime.strptime(data_modificacao, "%Y-%m-%dT%H:%M:%S")
    data_formatada = data_modificacao_datetime.strftime('%d/%m/%Y %H:%M:%S')

    if itens_pedidos is not None:
        itens_html = "".join(
            f"<li>{item['nome_consumivel']} - Quantidade: {item['quantidade']}</li>"
            for item in itens_pedidos
        )
    else:
        itens_html = ""

    html = f"""\
    <html>
    <body>
    <div style="max-width: 600px; margin: 20px auto; padding: 20px; background: #ffffff; border: 1px solid #ddd; border-radius: 7px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; color: #333;">
        <div style="background: #0275d8; color: #ffffff; padding: 10px; text-align: center; border-radius: 7px 7px 0 0;">
            <h2 style="margin: 0;">MedStock - Requerimento Entregue</h2>
        </div>
        <div style="padding: 20px; text-align: left;">
            <p>Prezado(a) {nome_utilizador_pedido},</p>
            <p>O requerimento <strong>REQ-{requerimento_id}</strong> foi entregue com sucesso.</p>
            <p>Entrega realizada por: <strong>{user_responsavel}</strong> em <strong>{data_formatada}</strong>.</p>
            <p>Por favor, valide a entrega para concluir o processo.</p>
            <h3>Itens do Requerimento:</h3>
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

    part2 = MIMEText(html, "html")
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password_email)
            server.sendmail(sender_email, message["To"], message.as_string())
        return True
    except Exception as e:
        return False
