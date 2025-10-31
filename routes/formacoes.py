from flask import Blueprint, request, jsonify
from models import db, Formacoes

formacoes_bp = Blueprint('formacoes', __name__)

#Criando nova formação

@formacoes_bp.route('/formacoes', methods=['POST'])
def criar_formacao():
    dados = request.get_json()
    nova_formacao = Formacoes(
        nome_formacao=dados['nome_formacao'],  # type: ignore
        carga_horaria=dados['carga_horaria']  # type: ignore
    )
    db.session.add(nova_formacao)
    db.session.commit()
    return jsonify({'message': 'Formação criada com sucesso.'}), 201

#Listando todas as formações

@formacoes_bp.route('/formacoes', methods=['GET'])
def listar_formacoes():
    formacoes = Formacoes.query.all()
    resultado = []
    for f in formacoes:
        resultado.append({
            'id_formacoes': f.id_formacoes,
            'nome_formacao': f.nome_formacao,
            'carga_horaria': f.carga_horaria
        })
    return jsonify(resultado), 200

#Atualizando uma formação existente
@formacoes_bp.route('/formacoes/<int:id>', methods=['PUT'])
def atualizar_formacao(id):
    formacao = Formacoes.query.get(id)
    if not formacao:
        return jsonify({'message': 'Formação não encontrada.'}), 404
    dados = request.get_json()
    formacao.nome_formacao = dados.get('nome_formacao', formacao.nome_formacao)
    formacao.carga_horaria = dados.get('carga_horaria', formacao.carga_horaria)
    db.session.commit()
    return jsonify({'message': 'Formação atualizada com sucesso.'}), 200

#Deletando uma formação
@formacoes_bp.route('/formacoes/<int:id>', methods=['DELETE'])
def deletar_formacao(id):
    formacao = Formacoes.query.get(id)
    if not formacao:
        return jsonify({'message': 'Formação não encontrada.'}), 404
    db.session.delete(formacao)
    db.session.commit()
    return jsonify({'message': 'Formação deletada com sucesso.'}), 200