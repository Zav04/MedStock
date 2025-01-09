from app import create_app
import os
from flask import Flask, jsonify


# Configurar o ambiente (default: 'development')
env = os.getenv('FLASK_ENV', 'development')

# Criar a aplicação com base no ambiente
app = create_app()

if __name__ == '__main__':
    # Configurar host, porta e modo debug
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')  # Default: localhost
    port = int(os.getenv('FLASK_RUN_PORT', 5000))     # Default: porta 5000
    debug = env == 'development'                     # Ativar debug apenas no ambiente de desenvolvimento
    
    print(f"Starting app in {env} mode...")
    app.run(host=host, port=port, debug=debug)

