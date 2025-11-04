from flask import Blueprint, request, jsonify
from models import db, Cursos

cursos_bp = Blueprint('cursos', __name__)

#Criando nova formação

@cursos_bp.route('/cursos', methods=['POST'])
def criar_cursos():
    dados = request.get_json()
    novo_curso = Cursos(
        nome_curso=dados['nome_curso'],  # type: ignore
        carga_horaria=dados['carga_horaria'],          # type: ignore
        palestrante=dados['palestrante']          # type: ignore
    )
    db.session.add(novo_curso)
    db.session.commit()
    return jsonify({'message': 'Formação criada com sucesso.'}), 201

#Listando todas as formações

@cursos_bp.route('/cursos', methods=['GET'])
def listar_cursos():
    cursos = Cursos.query.all()
    resultado = []
    for f in cursos:
        resultado.append({
            'id_cursos': f.id_cursos,
            'nome_curso': f.nome_curso,
            'carga_horaria': f.carga_horaria,
            'palestrante': f.palestrante
        })
    return jsonify(resultado), 200

#Atualizando uma formação existente
@cursos_bp.route('/cursos/<int:id>', methods=['PUT'])
def atualizar_cursos(id):
    cursos = Cursos.query.get(id)
    if not cursos:
        return jsonify({'message': 'Formação não encontrada.'}), 404
    dados = request.get_json()
    cursos.nome_curso = dados.get('nome_curso', cursos.nome_curso)
    cursos.carga_horaria = dados.get('carga_horaria', cursos.carga_horaria)
    cursos.palestrante = dados.get('palestrante', cursos.palestrante)
    db.session.commit()
    return jsonify({'message': 'Formação atualizada com sucesso.'}), 200

#Deletando uma formação
@cursos_bp.route('/cursos/<int:id>', methods=['DELETE'])
def deletar_cursos(id):
    cursos = Cursos.query.get(id)
    if not cursos:
        return jsonify({'message': 'Formação não encontrada.'}), 404
    db.session.delete(cursos)
    db.session.commit()
    return jsonify({'message': 'Formação deletada com sucesso.'}), 200