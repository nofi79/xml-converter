Sistema SaaS para conversão de arquivos XML dos eventos R4010 e R4020, validando contra XSDs oficiais, preenchendo campos obrigatórios com valores padrão, agrupando em lotes de 50 arquivos, compactando e permitindo download.

Tecnologias
Backend: Python 3.11+, FastAPI, xmlschema, lxml

Frontend: React 18, Vite, TailwindCSS

Outros: Node.js LTS, npm, Git, VS Code

Requisitos
Windows 10/11

Python 3.11+

Node.js LTS + npm

Git

VS Code com extensões recomendadas

Instalação
Backend
powershell
Copiar
Editar
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Coloque R4010.xsd e R4020.xsd em app/static_schemas/
uvicorn app.main:app --reload --port 8000
Frontend
powershell
Copiar
Editar
cd frontend
npm install
npm run dev
Uso
Acesse http://localhost:5173.

No painel R4010 ou R4020, selecione um arquivo .zip com XMLs.

Clique Converter.

Aguarde a barra de progresso atingir 100%.

Clique Baixar ZIP para receber os lotes processados.

Personalização
Substituir XSDs em backend/app/static_schemas/.

Ajustar regras de preenchimento em backend/app/converters/r4010.py e r4020.py.

Alterar cor principal no Tailwind: smokeBlue (#6785C1).

Produção
Configurar variáveis de ambiente.

Usar servidor de produção (Uvicorn/Gunicorn + Nginx).

Habilitar HTTPS e autenticação.

Armazenar jobs e arquivos em banco/S3.