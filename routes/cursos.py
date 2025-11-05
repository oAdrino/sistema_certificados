from flask import Blueprint, request, jsonify
from models import db, Cursos, Certificados, Professor
from datetime import datetime

cursos_bp = Blueprint('cursos', __name__)


# Rota de vinculação de curso a professor
@cursos_bp.route("/vincular_curso", methods=["POST"])
def vincular_curso():
    dados = request.get_json()
    id_professor = dados.get("id_professor")
    id_curso = dados.get("id_curso")
    data_realizacao = dados.get("data_realizacao")

    professor = Professor.query.get(id_professor)
    curso = Cursos.query.get(id_curso)

    if not professor or not curso:
        return jsonify({"error": "Professor ou Curso não encontrado"}), 404

    novo_vinculo = Certificados(
        id_professores=id_professor,  # pyright: ignore[reportCallIssue]
        id_cursos=id_curso,          # pyright: ignore[reportCallIssue]
        status="pendente",  # pyright: ignore[reportCallIssue]
        certificado_url=None,   # pyright: ignore[reportCallIssue]
        carga_horaria_total=curso.carga_horaria,  # pyright: ignore[reportCallIssue]
        data_realizacao=datetime.strptime(data_realizacao, "%Y-%m-%d") # pyright: ignore[reportCallIssue]
    )
    db.session.add(novo_vinculo)
    db.session.commit()

    return jsonify({"message": "Curso vinculado ao professor com sucesso."}), 201
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
