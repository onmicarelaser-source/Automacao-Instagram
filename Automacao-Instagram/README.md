# 🤖 Automacao-Instagram

Sistema automatizado para gerenciamento e publicação de conteúdo no Instagram com agendamento inteligente.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Usar](#como-usar)
- [Docker](#docker)
- [Testes](#testes)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## 🎯 Sobre o Projeto

O **Automacao-Instagram** é uma ferramenta poderosa desenvolvida em Python que automatiza o gerenciamento de contas no Instagram, permitindo:

- 📅 Agendamento inteligente de posts
- 📊 Análise de engajamento
- 🤖 Respostas automáticas a comentários
- 📈 Relatórios de desempenho
- 🎨 Edição e otimização de imagens
- 🔄 Sincronização entre múltiplas contas

## ⚡ Funcionalidades

### Core Features
- ✅ **Publicação Automática**: Agende e publique posts automaticamente
- ✅ **Agendador Inteligente**: Sistema de tarefas com cron scheduling
- ✅ **Multi-Conta**: Gerencie múltiplas contas simultaneamente
- ✅ **Análise de Engajamento**: Métricas e relatórios detalhados
- ✅ **Respostas Automáticas**: Bot para responder comentários e mensagens
- ✅ **Monitoramento**: Acompanhamento de métricas em tempo real

### Funcionalidades Avançadas
- 🎯 **Targeting**: Identificação de público-alvo
- 📊 **Dashboard**: Interface web para monitoramento
- 🔔 **Notificações**: Alertas via email e push
- 💾 **Backup Automático**: Backup de dados e configurações
- 🔒 **Segurança**: Autenticação e criptografia

## 🏗️ Estrutura do Projeto
Automacao-Instagram/
├── src/
│ ├── api/ # Integração com APIs
│ │ ├── instagram_api.py
│ │ ├── instagram_client.py
│ │ └── instagram_publisher.py
│ ├── models/ # Modelos de dados
│ │ ├── content.py
│ │ ├── post.py
│ │ └── user.py
│ ├── scheduler/ # Sistema de agendamento
│ │ ├── scheduler.py
│ │ ├── scheduler_manager.py
│ │ └── task_scheduler.py
│ └── utils/ # Utilitários
│ ├── config_manager.py
│ ├── file_manager.py
│ ├── health_check.py
│ ├── helpers.py
│ └── logger.py
├── tests/ # Testes automatizados
│ ├── test_instagram_publisher.py
│ └── test_scheduler.py
├── config/ # Configurações
│ └── config.json
├── scripts/ # Scripts de setup
│ ├── setup.ps1
│ └── setup.sh
├── main.py # Ponto de entrada
├── requirements.txt # Dependências
├── Dockerfile # Configuração Docker
├── docker-compose.yml # Orquestração Docker
├── .gitignore # Arquivos ignorados
└── README.md # Documentação

text

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask/FastAPI** - Framework web
- **APScheduler** - Agendamento de tarefas
- **Requests** - Requisições HTTP
- **SQLAlchemy** - ORM para banco de dados
- **Celery** - Fila de tarefas assíncronas

### APIs e Serviços
- **Instagram Graph API** - Integração oficial
- **Pillow** - Processamento de imagens
- **Pandas** - Análise de dados
- **JWT** - Autenticação segura

### Infraestrutura
- **Docker** - Containerização
- **PostgreSQL/MySQL** - Banco de dados
- **Redis** - Cache e filas
- **Nginx** - Servidor web/reverse proxy

## 📋 Pré-requisitos

Antes de começar, verifique se você possui:

- ✅ Python 3.8 ou superior
- ✅ pip (gerenciador de pacotes Python)
- ✅ Git (para clonar o repositório)
- ✅ Docker (opcional, para containerização)
- ✅ PostgreSQL ou MySQL (para produção)

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/onmicarelaser-source/Automacao-Instagram.git
cd Automacao-Instagram
2. Crie um ambiente virtual
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
3. Instale as dependências
bash
pip install -r requirements.txt
4. Configure as variáveis de ambiente
bash
# Crie o arquivo .env
cp .env.example .env

# Edite com suas credenciais
INSTAGRAM_USERNAME=seu_usuario
INSTAGRAM_PASSWORD=sua_senha
🔧 Configuração
Configuração do Instagram
Obtenha suas credenciais:

Acesse Instagram Developer Portal

Crie uma aplicação

Obtenha Access Token

Configure o arquivo config/config.json:

json
{
  "instagram": {
    "username": "seu_usuario",
    "password": "sua_senha",
    "access_token": "seu_token",
    "account_id": "seu_account_id"
  },
  "scheduler": {
    "timezone": "America/Sao_Paulo",
    "max_posts_per_day": 5,
    "default_interval": 3600
  },
  "logging": {
    "level": "INFO",
    "file": "logs/instagram_automation.log"
  }
}
💻 Como Usar
Executando a Aplicação
bash
# Modo desenvolvimento
python main.py

# Com scheduler ativado
python main.py --scheduler

# Modo debug
python main.py --debug
Comandos Úteis
bash
# Publicar um post imediatamente
python main.py --publish --image "caminho/imagem.jpg" --caption "Texto do post"

# Agendar um post
python main.py --schedule --image "imagem.jpg" --caption "Texto" --datetime "2026-01-01 10:00:00"

# Listar posts agendados
python main.py --list-scheduled

# Cancelar agendamento
python main.py --cancel --id 123
Exemplos de Uso
python
from src.api.instagram_publisher import InstagramPublisher
from src.scheduler.scheduler_manager import SchedulerManager

# Inicializar publisher
publisher = InstagramPublisher(
    username="seu_usuario",
    password="sua_senha"
)

# Publicar post
publisher.publish_post(
    image_path="caminho/imagem.jpg",
    caption="Texto do post",
    hashtags="#automacao #instagram"
)

# Agendar post
scheduler = SchedulerManager()
scheduler.schedule_post(
    image_path="imagem.jpg",
    caption="Post agendado",
    datetime="2026-01-01 10:00:00"
)
🐳 Docker
Construir a imagem
bash
docker build -t automacao-instagram .
Executar com Docker Compose
yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - INSTAGRAM_USERNAME=${INSTAGRAM_USERNAME}
      - INSTAGRAM_PASSWORD=${INSTAGRAM_PASSWORD}
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    restart: always
bash
docker-compose up -d
🧪 Testes
bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src tests/

# Teste específico
pytest tests/test_instagram_publisher.py
🤝 Contribuição
Fork o projeto

Crie sua branch: git checkout -b feature/nova-funcionalidade

Commit: git commit -m "feat: Adiciona nova funcionalidade"

Push: git push origin feature/nova-funcionalidade

Abra um Pull Request

📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

📞 Contato
Onmicare Laser

📧 Email: onmicarelaser@gmail.com

📱 Instagram: @onmicarelaser

🌐 GitHub: onmicarelaser-source

Feito com ❤️ pela equipe Onmicare Laser