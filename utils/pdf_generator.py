from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, Frame, Spacer
from datetime import datetime
import os

def gerar_certificado_pdf(nome_professor, cpf, nome_curso, carga_horaria, caminho_arquivo, cursos=None):
    
    # Página em modo paisagem
    c = canvas.Canvas(caminho_arquivo, pagesize=landscape(A4))
    largura, altura = landscape(A4)


    # Imagem de fundo
    c.drawImage("imagens/fundo_logo.png", 0, 0, width=largura, height=altura)

    # Titulo do certificado
    c.setFillColorRGB(0, 0.4, 0.6)
    c.setFont("Helvetica-Bold", 60)
    c.drawCentredString(largura / 2, altura - 180, "Certificado")

    # Texto do certificado
    styles = getSampleStyleSheet()
    style_texto = ParagraphStyle(
        "texto",
        parent=styles["Normal"],
        fontName="Times-Roman",  # Mudando para Times-Roman que tem suporte a negrito
        fontSize=22,
        leading=35,
        alignment=TA_CENTER,  # Centralizado
)   
    texto_html = f"""
    Certificamos para os devidos fins que o(a) Senhor(a)<br/> 
    <b><font size="28">{nome_professor.upper()}</font></b><br/> 
    portador(a) do CPF: {cpf},<br/>
    participou do Programa de Formação Continuada de Professores, da Rede 
    Municipal de Educação de Balneário Piçarras
    no ano de 2025, <br/>totalizando <b>{carga_horaria} horas.</b>
    """
    # Moldura de texto centralizado
    frame = Frame(
    x1=2.5 * cm,
    y1=altura / 2.5 - 80,
    width=largura - 5 * cm,
    height=8 * cm,
    showBoundary=0,
)
    frame.addFromList([Paragraph(texto_html, style_texto)], c)

    # === Assinatura e data ===
    style_ass = ParagraphStyle(
        "ass",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=20,
        alignment=TA_CENTER,
    )
    # Data e cidade (formatada em português)
    hoje = datetime.now()
    meses_pt = [
        "janeiro",
        "fevereiro",
        "março",
        "abril",
        "maio",
        "junho",
        "julho",
        "agosto",
        "setembro",
        "outubro",
        "novembro",
        "dezembro",
    ]
    data_formatada = f"{hoje.day:02d} de {meses_pt[hoje.month-1].capitalize()} de {hoje.year}."
    # Garantir cor preta para data e assinatura (título pode permanecer colorido)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Times-Roman", 14)

    # Margem direita (ajuste conforme desejar)
    margem_direita = 50  

    # Posição Y (altura vertical)
    pos_y = 150  

    # Desenha o texto alinhado à direita
    c.drawRightString(largura - margem_direita, pos_y, f"Balneário Piçarras (SC), {data_formatada}")

     # Linha e assinatura
    c.line(largura / 2 - 200, 80, largura / 2 + 200, 80)
    Paragraph(
        f"<b>Blaise Keniel da Cruz Duarte</b><br/>Secretário(a) de Educação",
        style_ass,
    ).wrapOn(c, largura, altura)
    # Nome e cargo em preto
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Times-Roman", 18)  # Fonte maior para o nome
    c.drawCentredString(largura / 2, 60, "Blaise Keniel da Cruz Duarte")
    c.setFont("Times-Roman", 14)  # Fonte menor para o cargo
    c.drawCentredString(largura / 2, 40, "Secretário(a) de Educação")
    c.showPage()

    # Segunda página: tabela de cursos vinculados
    if cursos:
        # Fundo da segunda página
        try:
            c.drawImage("imagens/fundo.png", 0, 0, width=largura, height=altura)
        except Exception:
            pass

        # Título da página
        c.setFont("Helvetica-Bold", 32)
        c.setFillColorRGB(0, 0.4, 0.6)
        c.drawCentredString(largura / 2, altura - 80, "Cursos Vinculados")

        # Cabeçalho da tabela
        c.setFont("Times-Bold", 16)
        c.setFillColorRGB(0, 0, 0)
        x0 = 60
        y0 = altura - 140
        c.drawString(x0, y0, "Data")
        c.drawString(x0 + 100, y0, "Nome do Curso")
        c.drawString(x0 + 350, y0, "Palestrante")
        c.drawString(x0 + 550, y0, "Carga Horária")

        # Linhas da tabela
        c.setFont("Times-Roman", 14)
        total_carga = 0
        y = y0 - 30
        for curso in cursos:
            data = curso.get("data", "")
            if isinstance(data, datetime):
                data = data.strftime("%d/%m/%Y")
            c.drawString(x0, y, str(data))
            c.drawString(x0 + 100, y, str(curso.get("nome", "")))
            c.drawString(x0 + 350, y, str(curso.get("palestrante", "")))
            carga = curso.get("carga_horaria", 0)
            c.drawString(x0 + 550, y, str(carga))
            total_carga += int(carga)
            y -= 25

        # Linha total
        c.setFont("Times-Bold", 16)
        c.drawString(x0 + 400, y - 10, "Total de Horas:")
        c.drawString(x0 + 550, y - 10, str(total_carga))

        c.showPage()
    c.save()
    
