from flask import Blueprint, request, jsonify
from models import db, Certificados, Professor, Cursos
from utils.pdf_generator import gerar_certificado_pdf
from flask import send_file
import os

certificados_bp = Blueprint('certificados', __name__)

#Criando certificado

@certificados_bp.route('/certificados', methods=['POST'])
def criar_certificado():
    dados = request.get_json()

    #Verificando se o professor existe
    professor = Professor.query.get(dados['id_professores'])
    curso = Cursos.query.get(dados['id_cursos'])

    if not professor or not curso:
        return jsonify({'error': 'Professor ou Curso não encontrado'}), 404
    
    novo_certificado = Certificados(
        id_professores=dados['id_professores'], # pyright: ignore[reportCallIssue]
        id_cursos=dados['id_cursos'],   # pyright: ignore[reportCallIssue]
        status=dados.get('status', 'pendente'), # type: ignore
        certificado_url=dados.get('certificado_url', ''), # pyright: ignore[reportCallIssue]
        carga_horaria_total=curso.carga_horaria # pyright: ignore[reportCallIssue]
    )

    db.session.add(novo_certificado)
    db.session.commit()

        #Gerando PDF do certificado
    nome_professor = professor.nome
    nome_curso = curso.nome_curso
    cpf = professor.cpf
    carga_horaria = curso.carga_horaria

    # Caminho onde o PDF será salvo

    caminho_arquivo = f"certificados/{nome_professor.replace(' ', '_')}_{nome_curso.replace(' ', '_')}.pdf"
    os.makedirs("certificados", exist_ok=True)

    gerar_certificado_pdf(nome_professor, cpf, nome_curso, carga_horaria, caminho_arquivo)

    #Atualizar URL no certificado

    novo_certificado.certificado_url = caminho_arquivo
    db.session.commit()

    return jsonify({'message': 'Certificado criado e PDF gerado com sucesso!'}), 201
#Listando certificados

@certificados_bp.route('/certificados', methods=['GET'])
def listar_certificados():
    certificados = Certificados.query.all()
    resultado = []
    for cert in certificados:
        resultado.append({
            'id_certificados': cert.id_certificados,
            'professor': cert.professor.nome,
            'cursos': cert.curso.nome_curso,
            'status': cert.status,
            'certificado_url': cert.certificado_url,
            'carga_horaria_total': cert.carga_horaria_total
        })

    return jsonify(resultado), 200

#Atualizando certificado
@certificados_bp.route('/certificados/<int:id>', methods=['PUT'])
def atualizar_certificado(id):
    cert = Certificados.query.get(id)

    if not cert:
        return jsonify({'error': 'Certificado não encontrado'}), 404

    dados = request.get_json()
    cert.status = dados.get('status', cert.status)
    cert.certificado_url = dados.get('certificado_url', cert.certificado_url)
    db.session.commit()

    return jsonify({'message': 'Certificado atualizado com sucesso!'}), 200

#Deletando certificado
@certificados_bp.route('/certificados/<int:id>', methods=['DELETE'])
def deletar_certificado(id):
    cert = Certificados.query.get(id)

    if not cert:
        return jsonify({'error': 'Certificado não encontrado'}), 404

    db.session.delete(cert)
    db.session.commit()

    return jsonify({'message': 'Certificado deletado com sucesso!'}), 200

#Baixando certificado PDF
@certificados_bp.route('/certificados/<int:id>/download', methods=['GET'])
def download_certificado(id):
    cert = Certificados.query.get(id)

    if not cert or not cert.certificado_url:
        return jsonify({'error': 'Certificado não encontrado'}), 404

    caminho_arquivo = cert.certificado_url
    
    if not caminho_arquivo or not os.path.exists(caminho_arquivo):
        return jsonify({'error': 'Arquivo do certificado não encontrado'}), 404

    return send_file(caminho_arquivo, as_attachment=True)


@certificados_bp.route('/certificados/<int:id_professor>', methods=['GET'])
def listar_certificados_por_professor(id_professor):
    certificados = Certificados.query.filter_by(id_professores=id_professor).all()

    if not certificados:
        return jsonify({'error': 'Nenhum certificado encontrado para este professor'}), 404
    
    resultado = []
    for cert in certificados:
        resultado.append({
            "id_certificado": cert.id_certificados,
            "nome_curso": cert.curso.nome_curso,
            "palestrante": cert.curso.palestrante,
            "carga_horaria": cert.curso.carga_horaria,
            "data_realizacao": cert.data_realizacao.strftime("%d/%m/%Y"),
            "status": cert.status
        })
    return jsonify(resultado), 200