from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def gerar_certificado_pdf(nome_professor, nome_formacao, carga_horaria, caminho_arquivo):
    c = canvas.Canvas(caminho_arquivo, pagesize=A4)
    largura, altura = A4

    # Titulo do certificado
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(largura / 2, altura - 100, "Certificado de Conclusão")

    # Texto do certificado

    c.setFont("Helvetica", 14)
    texto = f"Certificamos que {nome_professor} concluiu a formação \"{nome_formacao}\" com carga horária de {carga_horaria} horas."
    c.drawCentredString(largura / 2, altura - 150, texto)

    # Assinatura e logo
 
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(50, 100, "Assinatura Digital")
    c.drawString(largura - 200, 100, "Instituição XYZ")

    c.showPage()
    c.save()

