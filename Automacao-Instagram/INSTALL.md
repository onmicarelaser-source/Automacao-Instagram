---

## 📄 ARQUIVO 9: `INSTALL.md` (COMPLETO)

```markdown
# 📦 Guia de Instalação

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Conexão com internet

## 🚀 Instalação Rápida

### Windows

```powershell
# 1. Clone o repositório
git clone https://github.com/onmicarelaser-source/Automacao-Instagram.git
cd Automacao-Instagram

# 2. Crie ambiente virtual
python -m venv venv
venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure
copy .env.example .env
notepad .env

# 5. Execute
python main.py
Linux/Mac
bash
# 1. Clone o repositório
git clone https://github.com/onmicarelaser-source/Automacao-Instagram.git
cd Automacao-Instagram

# 2. Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
nano .env

# 5. Execute
python main.py
🐳 Instalação com Docker
bash
# 1. Clone o repositório
git clone https://github.com/onmicarelaser-source/Automacao-Instagram.git
cd Automacao-Instagram

# 2. Configure variáveis
cp .env.example .env
nano .env

# 3. Execute com Docker Compose
docker-compose up -d
🔧 Configuração
Arquivo .env
env
# Instagram Credentials
INSTAGRAM_USERNAME=seu_usuario
INSTAGRAM_PASSWORD=sua_senha

# API Settings
API_PORT=5000
API_HOST=0.0.0.0

# Scheduler Settings
SCHEDULER_TIMEZONE=America/Sao_Paulo
MAX_POSTS_PER_DAY=5
Arquivo config/config.json
json
{
  "instagram": {
    "username": "seu_usuario",
    "password": "sua_senha"
  },
  "scheduler": {
    "timezone": "America/Sao_Paulo",
    "max_posts_per_day": 5
  }
}
✅ Verificação da Instalação
bash
# Verificar Python
python --version

# Verificar pip
pip --version

# Verificar dependências
pip list

# Testar a aplicação
python main.py --help
🐛 Problemas Comuns
Erro: 'git' não é reconhecido
Solução: Instale o Git em https://git-scm.com/download/win

Erro: 'python' não é reconhecido
Solução: Instale o Python e adicione ao PATH

Erro: Falha ao instalar dependências
Solução: Atualize o pip: pip install --upgrade pip

Erro: Falha de autenticação no Instagram
Solução: Verifique suas credenciais no arquivo .env

📞 Suporte
📧 Email: onmicarelaser@gmail.com

📚 Documentação: README.md

Instalação concluída com sucesso! 🎉