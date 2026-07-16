# 🚀 Guia de Deploy

## 📋 Índice

- [Pré-requisitos](#pré-requisitos)
- [Deploy Local](#deploy-local)
- [Deploy com Docker](#deploy-com-docker)
- [Deploy em Servidor](#deploy-em-servidor)
- [Deploy na Nuvem](#deploy-na-nuvem)
- [Monitoramento](#monitoramento)
- [Backup](#backup)

## 📋 Pré-requisitos

### Requisitos Mínimos

- **CPU:** 1 core
- **RAM:** 1GB
- **Storage:** 2GB
- **Sistema:** Linux/Windows/Mac
- **Python:** 3.8+

### Softwares Necessários

- Python 3.8+
- Git
- Docker (opcional)
- PostgreSQL (opcional)
- Redis (opcional)

## 🖥️ Deploy Local

### 1. Clone o Repositório

```bash
git clone https://github.com/onmicarelaser-source/Automacao-Instagram.git
cd Automacao-Instagram
2. Configure o Ambiente
bash
# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt
3. Configure Variáveis
bash
# Crie arquivo .env
cp .env.example .env

# Edite com suas credenciais
nano .env
4. Execute
bash
# Modo produção
python main.py --production

# Modo desenvolvimento
python main.py --debug
🐳 Deploy com Docker
1. Build da Imagem
bash
docker build -t automacao-instagram .
2. Docker Compose
yaml
# docker-compose.yml
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
3. Execute
bash
docker-compose up -d
🌐 Deploy em Servidor
Ubuntu/Debian
bash
# 1. Atualize o sistema
sudo apt update && sudo apt upgrade -y

# 2. Instale dependências
sudo apt install python3 python3-pip python3-venv git -y

# 3. Clone o projeto
git clone https://github.com/onmicarelaser-source/Automacao-Instagram.git
cd Automacao-Instagram

# 4. Configure
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Crie serviço systemd
sudo nano /etc/systemd/system/instagram-bot.service
Serviço Systemd
ini
[Unit]
Description=Instagram Automation Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/Automacao-Instagram
Environment="PATH=/path/to/Automacao-Instagram/venv/bin"
ExecStart=/path/to/Automacao-Instagram/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
Inicie o Serviço
bash
sudo systemctl daemon-reload
sudo systemctl enable instagram-bot
sudo systemctl start instagram-bot
sudo systemctl status instagram-bot
☁️ Deploy na Nuvem
AWS EC2
bash
# 1. Crie uma instância EC2
# 2. Conecte via SSH
ssh -i seu-key.pem ubuntu@ip-da-instancia

# 3. Instale dependências
sudo apt update
sudo apt install python3 python3-pip git -y

# 4. Clone e configure
git clone https://github.com/onmicarelaser-source/Automacao-Instagram.git
cd Automacao-Instagram
pip3 install -r requirements.txt

# 5. Execute
python3 main.py
Google Cloud Platform
bash
# 1. Crie VM no Compute Engine
# 2. Conecte via SSH
gcloud compute ssh instancia --zone=us-central1-a

# 3. Siga os mesmos passos do AWS
Microsoft Azure
bash
# 1. Crie VM no Azure
# 2. Conecte via SSH
ssh usuario@ip-da-vm

# 3. Siga os mesmos passos
📊 Monitoramento
Health Check
bash
# Verificar status
curl http://localhost:5000/health

# Verificar métricas
curl http://localhost:5000/metrics

# Verificar logs
tail -f logs/instagram_automation.log
Prometheus + Grafana
yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
💾 Backup
Backup Automático
bash
# Script de backup
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR="/backups/instagram-bot"

mkdir -p $BACKUP_DIR

# Backup dos dados
tar -czf $BACKUP_DIR/data-$DATE.tar.gz data/

# Backup das configurações
tar -czf $BACKUP_DIR/config-$DATE.tar.gz config/

# Backup do banco
pg_dump -U user dbname > $BACKUP_DIR/db-$DATE.sql

# Limpar backups antigos (30 dias)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
Cron para Backup
bash
# Adicionar ao crontab
0 2 * * * /path/to/backup.sh
🔄 Atualizações
Atualizar via Git
bash
# Parar o serviço
sudo systemctl stop instagram-bot

# Atualizar código
git pull origin main

# Atualizar dependências
pip install -r requirements.txt

# Reiniciar serviço
sudo systemctl start instagram-bot
Atualizar via Docker
bash
docker-compose down
docker-compose pull
docker-compose up -d
🐛 Troubleshooting
Logs de Erro
bash
# Ver logs do serviço
sudo journalctl -u instagram-bot -f

# Ver logs do Docker
docker logs -f instagram-bot

# Ver logs da aplicação
tail -f logs/instagram_automation.log
Problemas Comuns
Problema	Solução
Porta em uso	Mude a porta no arquivo .env
Falha de autenticação	Verifique credenciais
Erro de API	Verifique token de acesso
Memória insuficiente	Aumente RAM da instância
📞 Suporte
📧 Email: onmicarelaser@gmail.com

📚 Documentação: claude.md

🐛 Issues: GitHub Issues

Deploy concluído com sucesso! 🚀