# Sistema de Gestão de Cursos e Certificados

Este projeto é um sistema web para gerenciamento de formações de professores e geração automática de certificados em PDF.

## Tecnologias utilizadas

- **Backend**: Flask (Python)
- **Frontend**: Next.js + TypeScript + Tailwind CSS
- **Banco de Dados**: PostgreSQL
- **PDF**: ReportLab
- **Hospedagem**: Render (backend), Vercel (frontend)

## Funcionalidades

- Cadastro de professores e formações
- Emissão de certificados com soma automática de carga horária
- Geração de certificados em PDF
- Download de certificados
- Listagem de certificados por professor
- (Em breve) Login administrativo e relatórios

## Como rodar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/oAdrino/sistema_certificados.git
   cd seu-repositorio

2. Crie e ative o ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # ou venv\Scripts\activate no Windows

3. Instale as dependências: 
    pip install -r requirements.txt
    
4. Configure o banco PostgreSQL e atualize a string de conexão no app.py.

5. Execute o servidor:
    python app.py
