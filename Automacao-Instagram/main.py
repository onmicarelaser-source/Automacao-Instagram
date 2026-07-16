#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sistema de Automação Total para Instagram
Usa Gemini + Claude + Canva + Instagram APIs
100% automático, sem intervenção manual
"""

import time
import logging
from datetime import datetime
from config.api_config import APIConfig
from criacao.orquestrador import OrquestradorConteudo
from publicador.instagram_publisher import InstagramPublisher
from agendador.scheduler import AgendaScheduler

# Configurar logs
logging.basicConfig(
    level=getattr(logging, APIConfig.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automacao.log'),
        logging.StreamHandler()
    ]
)

class AutomacaoInstagram:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.orquestrador = OrquestradorConteudo()
        self.publicador = InstagramPublisher()
        self.scheduler = AgendaScheduler()
        
        self.logger.info("=" * 60)
        self.logger.info("🤖 AUTOMAÇÃO TOTAL DO INSTAGRAM INICIADA")
        self.logger.info("=" * 60)
        self.logger.info(f"📅 Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.logger.info(f"📊 Postagens agendadas: {len(self.scheduler.agenda)}")
        self.logger.info("=" * 60)
    
    def processar_proximo_post(self):
        """Processa o próximo post da agenda"""
        post = self.scheduler.get_proximo_post()
        
        if not post:
            self.logger.info("📋 Nenhum post pendente no momento.")
            return False
        
        self.logger.info(f"🚀 Processando post: {post['tema']}")
        self.logger.info(f"   Data: {post['data']} {post['hora']}")
        self.logger.info(f"   Tipo: {post['tipo']}")
        self.logger.info(f"   Tom: {post['tom']}")
        
        try:
            # 1. Criar conteúdo
            self.logger.info("  📝 Criando conteúdo...")
            conteudo = self.orquestrador.criar_conteudo_completo(
                tema=post['tema'],
                tipo=post['tipo'],
                tom=post['tom']
            )
            
            if not conteudo:
                self.logger.error("❌ Falha ao criar conteúdo")
                return False
            
            # 2. Publicar
            self.logger.info("  📤 Publicando...")
            
            if post['tipo'] == 'post':
                sucesso = self.publicador.publicar_post(
                    conteudo['imagem_url'],
                    conteudo['legenda'] + "\n\n" + conteudo.get('hashtags', '')
                )
            elif post['tipo'] == 'story':
                sucesso = self.publicador.publicar_story(
                    conteudo['imagem_url'],
                    conteudo['legenda'][:100]
                )
            elif post['tipo'] == 'reel':
                # Para reel, precisamos de vídeo
                # Usando imagem como fallback
                sucesso = self.publicador.publicar_reel(
                    conteudo['imagem_url'],
                    conteudo['legenda']
                )
            else:
                sucesso = False
            
            if sucesso:
                self.scheduler.marcar_publicado(post)
                self.logger.info(f"✅ Post publicado com sucesso: {post['tema']}")
                return True
            else:
                self.logger.error(f"❌ Falha ao publicar: {post['tema']}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar post: {e}")
            return False
    
    def executar_loop(self):
        """Loop principal de execução"""
        self.logger.info("🔄 Iniciando loop de monitoramento...")
        
        while True:
            try:
                # Verificar próximo post
                if self.processar_proximo_post():
                    self.logger.info("⏳ Aguardando próximo post...")
                else:
                    self.logger.info("💤 Sem postagens pendentes. Verificando novamente...")
                
                # Aguardar antes da próxima verificação
                time.sleep(APIConfig.VERIFICAR_INTERVALO)
                
            except KeyboardInterrupt:
                self.logger.info("👋 Sistema interrompido pelo usuário")
                break
            except Exception as e:
                self.logger.error(f"❌ Erro no loop: {e}")
                time.sleep(60)  # Esperar 1 minuto e tentar novamente
    
    def adicionar_post_manual(self):
        """Adiciona post manualmente (para testes)"""
        print("\n📝 ADICIONAR POSTAGEM MANUAL")
        print("-" * 40)
        
        data = input("📅 Data (YYYY-MM-DD): ")
        hora = input("🕐 Hora (HH:MM): ")
        tema = input("📌 Tema: ")
        tipo = input("📂 Tipo (post/story/reel): ")
        tom = input("🎭 Tom (profissional/promocional/divertido/emocional): ")
        
        self.scheduler.adicionar_post(data, hora, tema, tipo, tom)
        print(f"✅ Postagem agendada para {data} às {hora}!")

if __name__ == "__main__":
    # Validar configurações
    try:
        APIConfig.validar()
    except Exception as e:
        print(f"❌ {e}")
        exit(1)
    
    # Criar pasta de logs
    import os
    os.makedirs("logs", exist_ok=True)
    
    # Iniciar sistema
    sistema = AutomacaoInstagram()
    
    # Menu
    print("\n" + "=" * 50)
    print("🤖 AUTOMAÇÃO TOTAL DO INSTAGRAM")
    print("=" * 50)
    print("1. 🚀 Iniciar modo automático (24/7)")
    print("2. 📝 Adicionar postagem manual")
    print("3. 📋 Ver agenda")
    print("4. ⚙️ Processar postagens pendentes agora")
    print("5. ❌ Sair")
    print("=" * 50)
    
    opcao = input("Escolha: ")
    
    if opcao == "1":
        sistema.executar_loop()
    elif opcao == "2":
        sistema.adicionar_post_manual()
    elif opcao == "3":
        print("\n📋 AGENDA:")
        for p in sistema.scheduler.agenda:
            status = "✅" if p.get("publicado") else "⏳"
            print(f"{status} {p['data']} {p['hora']} - {p['tema']} ({p['tipo']})")
    elif opcao == "4":
        sistema.processar_proximo_post()
    elif opcao == "5":
        print("👋 Até logo!")
    else:
        print("❌ Opção inválida!")
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Instagram Posts and Stories Automation - Main Entry Point
Author: Claude AI
Version: 1.0.0
Description: Sistema automatizado para publicação de posts e stories no Instagram
"""

import sys
import os
import signal
import time
import threading
from datetime import datetime
from typing import Optional

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.logger import setup_logger, get_logger
from src.utils.config_manager import ConfigManager
from src.scheduler.scheduler_manager import SchedulerManager
from src.api.instagram_publisher import InstagramPublisher
from src.models.post import Post, Story
from src.utils.health_check import HealthCheck

# Configuração global
logger = None
scheduler = None
publisher = None
health_check = None
running = True

def signal_handler(signum, frame):
    """
    Manipulador de sinais para encerramento gracioso
    """
    global running
    logger.warning(f"Sinal {signum} recebido. Encerrando aplicação...")
    running = False
    
    if scheduler:
        scheduler.stop()
    
    if publisher:
        publisher.close()
    
    logger.info("Aplicação encerrada com sucesso")
    sys.exit(0)

def initialize_application():
    """
    Inicializa todos os componentes da aplicação
    """
    global logger, scheduler, publisher, health_check
    
    # Configura o logger
    logger = setup_logger(
        log_level="INFO",
        log_file="./logs/automation.log",
        console_output=True
    )
    
    logger.info("=" * 80)
    logger.info("Instagram Automation System v1.0.0")
    logger.info("Iniciando aplicação...")
    logger.info("=" * 80)
    
    # Carrega configurações
    config_manager = ConfigManager("./config/config.json")
    config = config_manager.load_config()
    
    # Verifica ambiente
    logger.info(f"Ambiente: {'DEBUG' if config.get('debug', False) else 'PRODUCTION'}")
    logger.info(f"Timezone: {config.get('timezone', 'America/Sao_Paulo')}")
    
    # Inicializa Health Check
    health_check = HealthCheck()
    health_check.start_monitoring()
    
    # Inicializa Publisher
    publisher = InstagramPublisher()
    
    # Inicializa Scheduler
    scheduler = SchedulerManager(publisher, config)
    
    # Carrega histórico
    scheduler.load_history()
    
    return config

def main_loop():
    """
    Loop principal da aplicação
    """
    global running
    
    logger.info("Aplicação iniciada. Aguardando agendamentos...")
    logger.info(f"Posts agendados para: {scheduler.get_post_schedule()}")
    logger.info(f"Stories agendados para: {scheduler.get_story_schedule()}")
    
    # Executa tarefas pendentes imediatamente
    if scheduler.should_run_immediately():
        logger.info("Executando tarefas pendentes...")
        scheduler.run_pending_tasks()
    
    # Loop principal
    while running:
        try:
            # Executa tarefas agendadas
            scheduler.run_pending_tasks()
            
            # Health Check periódico
            if health_check:
                health_check.check_status()
            
            # Dorme por 60 segundos
            time.sleep(60)
            
        except KeyboardInterrupt:
            logger.info("Interrupção por teclado detectada")
            break
        except Exception as e:
            logger.error(f"Erro no loop principal: {str(e)}", exc_info=True)
            time.sleep(300)  # Espera 5 minutos antes de tentar novamente
    
    # Encerramento
    logger.info("Loop principal finalizado")

def run_once():
    """
    Executa uma única vez (para testes)
    """
    logger.info("Executando em modo single-run...")
    
    # Publica um post de teste
    test_post = Post(
        image_path="./assets/posts/test.jpg",
        caption="Teste de publicação automatizada!\n\n#Teste #Automacao #Instagram",
        hashtags=["Teste", "Automacao", "Instagram"],
        scheduled_time=datetime.now()
    )
    
    publisher.publish_post(test_post)
    
    # Publica um story de teste
    test_story = Story(
        image_path="./assets/stories/test.jpg",
        duration=15,
        scheduled_time=datetime.now()
    )
    
    publisher.publish_story(test_story)
    
    logger.info("Execução única finalizada")

def main():
    """
    Função principal
    """
    try:
        # Configura manipuladores de sinal
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Inicializa aplicação
        config = initialize_application()
        
        # Verifica argumentos de linha de comando
        if len(sys.argv) > 1 and sys.argv[1] == "--once":
            run_once()
            return
        
        # Inicia o loop principal
        main_loop()
        
    except Exception as e:
        if logger:
            logger.error(f"Erro fatal na aplicação: {str(e)}", exc_info=True)
        else:
            print(f"Erro fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()