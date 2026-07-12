# Script de configuração para Instagram Automation (Windows)
# Versão: 1.0.0

Write-Host "=== Instagram Automation Setup ===" -ForegroundColor Cyan
Write-Host "Iniciando configuração..." -ForegroundColor Yellow

# Verifica Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python não encontrado. Instale o Python 3.8 ou superior." -ForegroundColor Red
    exit 1
}

# Verifica pip
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ pip encontrado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "pip não encontrado. Instalando..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}

# Cria ambiente virtual
Write-Host "Criando ambiente virtual..." -ForegroundColor Yellow
python -m venv venv

# Ativa ambiente virtual
Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Atualiza pip
Write-Host "Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Instala dependências
Write-Host "Instalando dependências..." -ForegroundColor Yellow
pip install -r requirements.txt

# Cria diretórios
Write-Host "Criando diretórios..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "assets\posts" | Out-Null
New-Item -ItemType Directory -Force -Path "assets\stories" | Out-Null
New-Item -ItemType Directory -Force -Path "config" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "backups" | Out-Null

# Cria arquivo .env
if (-not (Test-Path ".env")) {
    Write-Host "Criando arquivo .env..." -ForegroundColor Yellow
    @"
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
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✓ Arquivo .env criado" -ForegroundColor Green
} else {
    Write-Host "✓ Arquivo .env já existe" -ForegroundColor Green
}

# Verifica configuração
Write-Host "Verificando configuração..." -ForegroundColor Yellow
if (Test-Path "config\config.json") {
    Write-Host "✓ Arquivo de configuração encontrado" -ForegroundColor Green
} else {
    Write-Host "⚠ Arquivo de configuração não encontrado" -ForegroundColor Yellow
    Write-Host "Crie manualmente o config/config.json" -ForegroundColor Yellow
}

# Testa importações
Write-Host "Testando importações..." -ForegroundColor Yellow
try {
    python -c "import src; print('✓ Importações OK')" 2>$null
} catch {
    Write-Host "⚠ Erro nas importações" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Setup Concluído! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Edite o arquivo .env com suas credenciais" -ForegroundColor White
Write-Host "2. Coloque suas artes em assets\posts\ e assets\stories\" -ForegroundColor White
Write-Host "3. Execute: python main.py" -ForegroundColor White
Write-Host ""
Write-Host "Para iniciar a automação:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""
Write-Host "Para testes:" -ForegroundColor Yellow
Write-Host "  pytest tests/" -ForegroundColor White