from flask import Blueprint, request, jsonify
from models import db, Professor

professores_bp = Blueprint('professores', __name__)


@professores_bp.route('/professores', methods=['POST'])
def adicionar_professor():
    dados = request.get_json()
    novo_professor = Professor(
        nome = dados['nome'], # type: ignore
        cpf = dados['cpf'], # pyright: ignore[reportCallIssue]
        num_contrato = dados['num_contrato'], # type: ignore
        lotacao = dados['lotacao'], # type: ignore
        cargo_funcao = dados['cargo_funcao'] # type: ignore
    )
    db.session.add(novo_professor)
    db.session.commit()
    return jsonify({'message': 'Professor adicionado com sucesso.'}), 201

@professores_bp.route('/professores', methods=['GET'])
def listar_professores():
    professores = Professor.query.all()
    resultado = []
    for prof in professores:
        resultado.append({
            'id_professores': prof.id_professores,
            'nome': prof.nome,
            'cpf': prof.cpf,
            'num_contrato': prof.num_contrato,
            'lotacao': prof.lotacao,
            'cargo_funcao': prof.cargo_funcao
        })
    return jsonify(resultado), 200

@professores_bp.route('/professores/<int:id>', methods=['PUT'])
def atualizar_professor(id):
    prof = Professor.query.get(id)
    if not prof:
        return jsonify({'message': 'Professor não encontrado.'}), 404
    dados = request.get_json()
    prof.nome = dados.get('nome', prof.nome)
    prof.cpf = dados.get('cpf', prof.cpf)
    prof.num_contrato = dados.get('num_contrato', prof.num_contrato)
    prof.lotacao = dados.get('lotacao', prof.lotacao)
    prof.cargo_funcao = dados.get('cargo_funcao', prof.cargo_funcao)
    db.session.commit()
    return jsonify({'message': 'Professor atualizado com sucesso.'}), 200


@professores_bp.route('/professores/<int:id>', methods=['DELETE'])
def deletar_professor(id):
    prof = Professor.query.get(id)
    if not prof:
        return jsonify({'message': 'Professor não encontrado.'}), 404
    db.session.delete(prof)
    db.session.commit()
    return jsonify({'message': 'Professor deletado com sucesso.'}), 200