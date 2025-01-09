from flask import Blueprint, jsonify, request
from .models import db, Fornecedor, Produto, Requerimento, Pedido
from sqlalchemy import text, func

api = Blueprint('api', __name__)

# Helper function to format query results
def format_requerimentos_query(query_result):
    return [
        {
            'fornecedor_id': r.fornecedor_id,
            'em_espera': r.em_espera,
            'em_preparacao': r.em_preparacao,
            'enviado': r.enviado,
            'finalizado': r.finalizado,
        }
        for r in query_result
    ]

# Rota para obter todos os fornecedores
@api.route('/fornecedores', methods=['GET'])
def get_fornecedores():
    fornecedores = Fornecedor.query.all()
    return jsonify([
        {
            'id': f.id_fornecedor,
            'nome': f.nome,
            'categoria': f.categoria,
            'tempo_min': f.tempo_min
        } for f in fornecedores
    ])

# Rota para obter os produtos de um fornecedor específico
@api.route('/fornecedores/<int:fornecedor_id>/produtos', methods=['GET'])
def get_produtos_por_fornecedor(fornecedor_id):
    fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
    produtos = Produto.query.filter_by(fornecedor_id=fornecedor_id).all()

    return jsonify({
        'fornecedor': {
            'id': fornecedor.id_fornecedor,
            'nome': fornecedor.nome
        },
        'produtos': [
            {
                'id_produto': produto.id_produto,
                'nome': produto.nome,
                'quantidade': produto.quantidade
            }
            for produto in produtos
        ]
    })

# Rota para obter os requerimentos por fornecedor e estado
@api.route('/fornecedores/requerimentos', methods=['GET'])
def get_requerimentos_por_fornecedor():
    try:
        # SQL para contar os requerimentos por estado e fornecedor
        query = text("""
        SELECT 
            fornecedor_id,
            estado,
            COUNT(*) AS count
        FROM requerimentos
        GROUP BY fornecedor_id, estado;
        """)
        
        result = db.session.execute(query).fetchall()

        # Estruturando os dados para retorno
        requerimentos_por_fornecedor = {}

        for row in result:
            fornecedor_id = row[0]  # ou row['fornecedor_id']
            estado = row[1].lower().replace(' ', '_').replace('ç', 'c').replace('ã', 'a')    # Ex: "EM ESPERA" -> "em_espera"
            count = row[2]  # ou row['count']

            # Inicializa o dicionário do fornecedor, se ainda não existir
            if fornecedor_id not in requerimentos_por_fornecedor:
                requerimentos_por_fornecedor[fornecedor_id] = {
                    'em_espera': 0,
                    'em_preparacao': 0,
                    'enviado': 0,
                    'finalizado': 0
                }

            # Atualiza o estado correspondente
            requerimentos_por_fornecedor[fornecedor_id][estado] = count

        # Retorna os dados em formato JSON
        return jsonify(requerimentos_por_fornecedor)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Nova rota para buscar requerimentos em espera, com produtos e suas quantidades
@api.route('/fornecedores/<int:fornecedor_id>/requerimentos/em_espera', methods=['GET'])
def get_requerimentos_em_espera(fornecedor_id):
    try:
        # SQL para pegar os requerimentos em espera para um fornecedor específico
        query = text("""
        SELECT 
            r.id_requerimento,
            p.id_produto,
            p.nome AS produto_nome,
            pd.quantidade AS quantidade_pedida
        FROM requerimentos r
        JOIN pedidos pd ON r.id_requerimento = pd.requerimento_id
        JOIN produtos p ON pd.produto_id = p.id_produto
        WHERE r.estado = 'EM ESPERA' AND r.fornecedor_id = :fornecedor_id;
        """)

        result = db.session.execute(query, {'fornecedor_id': fornecedor_id}).fetchall()

        # Organizando os dados para retorno
        requerimentos = {}
        
        for row in result:
            requerimento_id = row[0]
            produto_id = row[1]
            produto_nome = row[2]
            quantidade_pedida = row[3]

            # Se o requerimento ainda não foi adicionado ao dicionário
            if requerimento_id not in requerimentos:
                requerimentos[requerimento_id] = {
                    'id_requerimento': requerimento_id,
                    'produtos': []
                }

            # Adicionando o produto ao requerimento
            requerimentos[requerimento_id]['produtos'].append({
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'quantidade_pedida': quantidade_pedida
            })

        # Convertendo o dicionário de requerimentos para lista e retornando como JSON
        return jsonify(list(requerimentos.values()))

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
# Nova rota para buscar requerimentos em espera, com produtos e suas quantidades
@api.route('/fornecedores/<int:fornecedor_id>/requerimentos/em_preparacao', methods=['GET'])
def get_requerimentos_em_preparacao(fornecedor_id):
    try:
        # SQL para pegar os requerimentos em espera para um fornecedor específico
        query = text("""
        SELECT 
            r.id_requerimento,
            p.id_produto,
            p.nome AS produto_nome,
            pd.quantidade AS quantidade_pedida
        FROM requerimentos r
        JOIN pedidos pd ON r.id_requerimento = pd.requerimento_id
        JOIN produtos p ON pd.produto_id = p.id_produto
        WHERE r.estado = 'EM PREPARAÇÃO' AND r.fornecedor_id = :fornecedor_id;
        """)

        result = db.session.execute(query, {'fornecedor_id': fornecedor_id}).fetchall()

        # Organizando os dados para retorno
        requerimentos = {}
        
        for row in result:
            requerimento_id = row[0]
            produto_id = row[1]
            produto_nome = row[2]
            quantidade_pedida = row[3]

            # Se o requerimento ainda não foi adicionado ao dicionário
            if requerimento_id not in requerimentos:
                requerimentos[requerimento_id] = {
                    'id_requerimento': requerimento_id,
                    'produtos': []
                }

            # Adicionando o produto ao requerimento
            requerimentos[requerimento_id]['produtos'].append({
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'quantidade_pedida': quantidade_pedida
            })

        # Convertendo o dicionário de requerimentos para lista e retornando como JSON
        return jsonify(list(requerimentos.values()))

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Nova rota para buscar requerimentos enviados, com produtos e suas quantidades
@api.route('/fornecedores/<int:fornecedor_id>/requerimentos/enviado', methods=['GET'])
def get_requerimentos_enviados(fornecedor_id):
    try:
        # SQL para pegar os requerimentos enviados para um fornecedor específico
        query = text("""
        SELECT 
            r.id_requerimento,
            p.id_produto,
            p.nome AS produto_nome,
            pd.quantidade AS quantidade_pedida
        FROM requerimentos r
        JOIN pedidos pd ON r.id_requerimento = pd.requerimento_id
        JOIN produtos p ON pd.produto_id = p.id_produto
        WHERE r.estado = 'ENVIADO' AND r.fornecedor_id = :fornecedor_id;
        """)

        result = db.session.execute(query, {'fornecedor_id': fornecedor_id}).fetchall()

        # Organizando os dados para retorno
        requerimentos = {}
        
        for row in result:
            requerimento_id = row[0]
            produto_id = row[1]
            produto_nome = row[2]
            quantidade_pedida = row[3]

            # Se o requerimento ainda não foi adicionado ao dicionário
            if requerimento_id not in requerimentos:
                requerimentos[requerimento_id] = {
                    'id_requerimento': requerimento_id,
                    'produtos': []
                }

            # Adicionando o produto ao requerimento
            requerimentos[requerimento_id]['produtos'].append({
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'quantidade_pedida': quantidade_pedida
            })

        # Convertendo o dicionário de requerimentos para lista e retornando como JSON
        return jsonify(list(requerimentos.values()))

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Nova rota para buscar requerimentos em espera, com produtos e suas quantidades
@api.route('/fornecedores/<int:fornecedor_id>/requerimentos/finalizado', methods=['GET'])
def get_requerimentos_finalizados(fornecedor_id):
    try:
        # SQL para pegar os requerimentos em espera para um fornecedor específico
        query = text("""
        SELECT 
            r.id_requerimento,
            p.id_produto,
            p.nome AS produto_nome,
            pd.quantidade AS quantidade_pedida
        FROM requerimentos r
        JOIN pedidos pd ON r.id_requerimento = pd.requerimento_id
        JOIN produtos p ON pd.produto_id = p.id_produto
        WHERE r.estado = 'FINALIZADO' AND r.fornecedor_id = :fornecedor_id;
        """)

        result = db.session.execute(query, {'fornecedor_id': fornecedor_id}).fetchall()

        # Organizando os dados para retorno
        requerimentos = {}
        
        for row in result:
            requerimento_id = row[0]
            produto_id = row[1]
            produto_nome = row[2]
            quantidade_pedida = row[3]

            # Se o requerimento ainda não foi adicionado ao dicionário
            if requerimento_id not in requerimentos:
                requerimentos[requerimento_id] = {
                    'id_requerimento': requerimento_id,
                    'produtos': []
                }

            # Adicionando o produto ao requerimento
            requerimentos[requerimento_id]['produtos'].append({
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'quantidade_pedida': quantidade_pedida
            })

        # Convertendo o dicionário de requerimentos para lista e retornando como JSON
        return jsonify(list(requerimentos.values()))

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/requerimentos/<int:id>/estado', methods=['PUT'])
def atualizar_estado_requerimento(id):
    try:
        # Logando os cabeçalhos para verificação
        print("Cabeçalhos recebidos:", request.headers)

        # Verificando se o conteúdo da requisição é JSON
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 415

        data = request.get_json()  # Extraí o JSON do corpo da requisição
        novo_estado = data.get('estado')

        if not novo_estado:
            return jsonify({'error': 'Estado é obrigatório'}), 400

        if novo_estado not in ['EM ESPERA', 'EM PREPARAÇÃO', 'ENVIADO', 'FINALIZADO']:
            return jsonify({'error': 'Estado inválido'}), 400

        # Buscar requerimento pelo ID
        requerimento = Requerimento.query.get(id)
        if not requerimento:
            return jsonify({'error': 'Requerimento não encontrado'}), 404

        # Atualizar o estado
        requerimento.estado = novo_estado
        db.session.commit()

        return jsonify({'message': 'Estado atualizado com sucesso'}), 200

    except Exception as e:
        print(f"Erro ao atualizar estado: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Nova rota para finalizar o requerimento e atualizar a quantidade dos produtos
@api.route('/requerimentos/<int:requerimento_id>/finalizar', methods=['PUT'])
def finalizar_requerimento(requerimento_id):
    try:
        # Verificando se o conteúdo da requisição é JSON
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 415

        # Extraindo os dados da requisição
        data = request.get_json()
        produtos_quantidade = data.get('produtos')  # Espera uma lista com produto_id e quantidade

        if not produtos_quantidade:
            return jsonify({'error': 'Produtos e suas quantidades são obrigatórios'}), 400

        # Buscar o requerimento pelo ID
        requerimento = Requerimento.query.get(requerimento_id)
        if not requerimento:
            return jsonify({'error': 'Requerimento não encontrado'}), 404

        # Atualizar o estado do requerimento para 'FINALIZADO'
        requerimento.estado = 'FINALIZADO'
        db.session.commit()

        # Processar cada produto e atualizar a quantidade disponível no estoque
        for produto_info in produtos_quantidade:
            produto_id = produto_info.get('produto_id')
            quantidade_pedida = produto_info.get('quantidade')

            if not produto_id or not quantidade_pedida:
                return jsonify({'error': 'Produto ID e Quantidade são obrigatórios'}), 400

            # Buscar o produto pelo ID
            produto = Produto.query.get(produto_id)
            if not produto:
                return jsonify({'error': f'Produto com ID {produto_id} não encontrado'}), 404

            # Verificar se a quantidade pedida é válida (não pode ser maior que o estoque)
            if produto.quantidade < quantidade_pedida:
                return jsonify({'error': f'Quantidade pedida para o produto {produto.nome} é maior que o estoque disponível'}), 400

            # Subtrair a quantidade pedida do estoque
            produto.quantidade -= quantidade_pedida
            print(f"Atualizando produto {produto.nome}, nova quantidade: {produto.quantidade}")  # Adicionando log
            db.session.commit()

        # Retornar sucesso
        return jsonify({'message': 'Requerimento finalizado e quantidades atualizadas com sucesso'}), 200

    except Exception as e:
        # Captura a exceção e faz o rollback
        db.session.rollback()
        print(f"Erro ao finalizar requerimento: {str(e)}")  # Log detalhado do erro
        return jsonify({'error': str(e)}), 500

@api.route('/fornecedores/produtos', methods=['GET'])
def get_produtos_de_todos_os_fornecedores():
    fornecedores = Fornecedor.query.all()  # Pega todos os fornecedores
    fornecedores_produtos = []

    for fornecedor in fornecedores:
        produtos = Produto.query.filter_by(fornecedor_id=fornecedor.id_fornecedor).all()
        fornecedores_produtos.append({
            'fornecedor': {
                'id': fornecedor.id_fornecedor,
                'nome': fornecedor.nome,
                'tempo': fornecedor.tempo_min
                
            },
            'produtos': [
                {
                    'id_produto': produto.id_produto,
                    'nome': produto.nome,
                    'quantidade': produto.quantidade
                }
                for produto in produtos
            ]
        })

    return jsonify(fornecedores_produtos)

@api.route('/requerimentos/<int:requerimento_id>', methods=['GET'])
def get_estado_requerimento(requerimento_id):
    try:
        # Buscar o requerimento pelo ID
        requerimento = Requerimento.query.get_or_404(requerimento_id)

        # Retornar o estado do requerimento
        return jsonify({
            'id_requerimento': requerimento.id_requerimento,
            'estado': requerimento.estado
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@api.route('/requerimentos/pedidos', methods=['POST'])
def criar_requerimento_com_pedidos():
    try:
        # Verificando se o conteúdo da requisição é JSON
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 415

        # Extraindo os dados do JSON enviado na requisição
        pedidos = request.get_json()

        # Verificar se é uma lista e contém pelo menos um pedido
        if not isinstance(pedidos, list) or len(pedidos) == 0:
            return jsonify({'error': 'Uma lista de pedidos é obrigatória'}), 400

        # Validar que todos os itens têm os campos necessários e que o fornecedor é consistente
        fornecedor_id = None
        for pedido in pedidos:
            if not isinstance(pedido, dict):
                return jsonify({'error': 'Cada pedido deve ser um objeto JSON'}), 400

            # Extrair campos obrigatórios
            pedido_fornecedor_id = pedido.get('fornecedor_id')
            produto_id = pedido.get('produto_id')
            quantidade = pedido.get('quantidade')

            if not pedido_fornecedor_id or not produto_id or not quantidade:
                return jsonify({'error': 'Fornecedor ID, Produto ID e Quantidade são obrigatórios para cada pedido'}), 400

            # Garantir que o fornecedor_id seja consistente entre os pedidos
            if fornecedor_id is None:
                fornecedor_id = pedido_fornecedor_id
            elif fornecedor_id != pedido_fornecedor_id:
                return jsonify({'error': 'Todos os pedidos devem pertencer ao mesmo fornecedor'}), 400

        # Criar o novo requerimento com estado 'EM ESPERA'
        novo_requerimento = Requerimento(
            fornecedor_id=fornecedor_id,
            estado='EM ESPERA'
        )

        # Adicionar o novo requerimento no banco de dados
        db.session.add(novo_requerimento)
        db.session.flush()  # Garante que o requerimento_id seja gerado

        # Obter o id_requerimento gerado
        id_requerimento = novo_requerimento.requerimento_id

        # Criar os pedidos associados ao mesmo requerimento
        pedidos_para_inserir = [
            Pedido(
                requerimento_id=id_requerimento,
                produto_id=pedido['produto_id'],
                fornecedor_id=fornecedor_id,
                quantidade=pedido['quantidade']
            )
            for pedido in pedidos
        ]

        # Adicionando todos os pedidos ao banco de dados
        db.session.bulk_save_objects(pedidos_para_inserir)

        # Commit para salvar no banco de dados
        db.session.commit()

        # Retornar a resposta com sucesso
        return jsonify({'message': 'Requerimento e pedidos criados com sucesso', 'requerimento_id': id_requerimento}), 201

    except Exception as e:
        # Captura qualquer erro e faz o rollback para evitar dados inconsistentes
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
