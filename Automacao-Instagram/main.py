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