from flask import Blueprint, request, jsonify
from models import db, Certificados, Professor, Formacoes
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
    formacao = Formacoes.query.get(dados['id_formacoes'])

    if not professor or not formacao:
        return jsonify({'error': 'Professor ou Formação não encontrado'}), 404
    
    novo_certificado = Certificados(
        id_professores=dados['id_professores'], # pyright: ignore[reportCallIssue]
        id_formacoes=dados['id_formacoes'], # pyright: ignore[reportCallIssue]
        status=dados.get('status', 'pendente'), # type: ignore
        certificado_url=dados.get('certificado_url', ''), # pyright: ignore[reportCallIssue]
        carga_horaria_total=formacao.carga_horaria # pyright: ignore[reportCallIssue]
    )

    db.session.add(novo_certificado)
    db.session.commit()

        #Gerando PDF do certificado
    nome_professor = professor.nome
    nome_formacao = formacao.nome_formacao
    carga_horaria = formacao.carga_horaria

    # Caminho onde o PDF será salvo

    caminho_arquivo = f"certificados/{nome_professor.replace(' ', '_')}_{nome_formacao.replace(' ', '_')}.pdf"
    os.makedirs("certificados", exist_ok=True)

    gerar_certificado_pdf(nome_professor, nome_formacao, carga_horaria, caminho_arquivo)

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
            'formacao': cert.formacao.nome_formacao,
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


@certificados_bp.route('/certificados/professor/<int:id>', methods=['GET'])
def listar_certificados_por_professor(id):
    professor = Professor.query.get(id)
    if not professor:
        return jsonify({'error': 'Professor não encontrado'}), 404
    
    certificados = Certificados.query.filter_by(id_professores=id).all()
    resultado = []
    for cert in certificados:
        resultado.append({
            'id_certificados': cert.id_certificados,
            'formacao': cert.formacao.nome_formacao,
            'status': cert.status,
            'certificado_url': cert.certificado_url,
            'carga_horaria_total': cert.carga_horaria_total
        })
    return jsonify({
        'professor': professor.nome,
        'certificados': resultado
    }), 200