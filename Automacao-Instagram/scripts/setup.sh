#!/bin/bash

# Script de configuração para Instagram Automation
# Versão: 1.0.0

echo "=== Instagram Automation Setup ==="
echo "Iniciando configuração..."

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 não encontrado. Instale o Python 3.8 ou superior."
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"

# Verifica pip
if ! command -v pip3 &> /dev/null; then
    echo "pip3 não encontrado. Instalando..."
    python3 -m ensurepip --upgrade
fi

echo "✓ pip encontrado: $(pip3 --version)"

# Cria ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv

# Ativa ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Atualiza pip
echo "Atualizando pip..."
pip install --upgrade pip

# Instala dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Cria diretórios
echo "Criando diretórios..."
mkdir -p assets/posts assets/stories config logs backups

# Cria arquivo .env
if [ ! -f .env ]; then
    echo "Criando arquivo .env..."
    cat > .env << EOL
# Instagram Credentials
INSTAGRAM_USERNAME=seu_usuario_aqui
INSTAGRAM_PASSWORD=sua_senha_aqui
INSTAGRAM_ACCOUNT_ID=seu_account_id_aqui

# API Keys
CANVA_API_KEY=sua_api_key_canva_aqui
FACEBOOK_ACCESS_TOKEN=seu_token_facebook_aqui

# Scheduling
POST_TIME=08:00
STORY_TIME=18:00
TIMEZONE=America/Sao_Paulo
EOL
    echo "✓ Arquivo .env criado"
else
    echo "✓ Arquivo .env já existe"
fi

# Verifica configuração
echo "Verificando configuração..."
if [ -f config/config.json ]; then
    echo "✓ Arquivo de configuração encontrado"
else
    echo "⚠ Arquivo de configuração não encontrado"
    echo "Copiando configuração padrão..."
    cp config/config.json.example config/config.json 2>/dev/null || echo "Crie manualmente o config/config.json"
fi

# Testa importações
echo "Testando importações..."
python -c "import src; print('✓ Importações OK')" 2>/dev/null || echo "⚠ Erro nas importações"

echo ""
echo "=== Setup Concluído! ==="
echo ""
echo "Próximos passos:"
echo "1. Edite o arquivo .env com suas credenciais"
echo "2. Coloque suas artes em assets/posts/ e assets/stories/"
echo "3. Execute: python main.py"
echo ""
echo "Para iniciar a automação:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Para testes:"
echo "  pytest tests/"