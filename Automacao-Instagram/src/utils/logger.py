#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Logger Module - Configuração e gerenciamento de logs
Version: 1.0.0
"""

import os
import sys
import logging
import logging.handlers
from datetime import datetime
from typing import Optional

# Configuração global do logger
_loggers = {}
_logger_initialized = False

def setup_logger(
    log_level: str = "INFO",
    log_file: str = "./logs/automation.log",
    console_output: bool = True,
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Configura e retorna um logger
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Caminho do arquivo de log
        console_output: Se deve exibir no console
        max_bytes: Tamanho máximo do arquivo de log
        backup_count: Número de backups
    
    Returns:
        Logger configurado
    """
    global _logger_initialized
    
    # Cria o diretório de logs se não existir
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # Configura o nível de log
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Cria o logger principal
    logger = logging.getLogger("InstagramAutomation")
    logger.setLevel(level)
    
    # Remove handlers existentes para evitar duplicação
    if logger.handlers:
        logger.handlers.clear()
    
    # Formato do log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo (com rotação)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para console
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    _logger_initialized = True
    
    # Log inicial
    logger.info("=" * 80)
    logger.info("Logger inicializado")
    logger.info(f"Nível de log: {log_level}")
    logger.info(f"Arquivo de log: {log_file}")
    logger.info(f"Console: {'Ativado' if console_output else 'Desativado'}")
    logger.info("=" * 80)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger para um módulo específico
    
    Args:
        name: Nome do módulo
    
    Returns:
        Logger configurado
    """
    if not _logger_initialized:
        # Se o logger principal não foi inicializado, configura com defaults
        setup_logger()
    
    # Cria um logger com o nome do módulo
    if name in _loggers:
        return _loggers[name]
    
    logger = logging.getLogger(f"InstagramAutomation.{name}")
    _loggers[name] = logger
    
    return logger

class LoggerContext:
    """
    Contexto para gerenciamento de logs
    """
    
    def __init__(self, logger: logging.Logger, operation: str):
        """
        Inicializa o contexto
        
        Args:
            logger: Logger a ser usado
            operation: Nome da operação
        """
        self.logger = logger
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        """
        Entra no contexto
        """
        self.start_time = datetime.now()
        self.logger.info(f"Iniciando {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Sai do contexto
        """
        duration = datetime.now() - self.start_time
        if exc_type:
            self.logger.error(f"{self.operation} falhou após {duration.total_seconds():.2f}s")
        else:
            self.logger.info(f"{self.operation} concluído em {duration.total_seconds():.2f}s")

# Para testes
if __name__ == "__main__":
    # Testa o logger
    logger = setup_logger(log_level="DEBUG", console_output=True)
    logger.debug("Mensagem de debug")
    logger.info("Mensagem de info")
    logger.warning("Mensagem de warning")
    logger.error("Mensagem de error")
    
    # Testa o contexto
    with LoggerContext(logger, "Operação de teste"):
        import time
        time.sleep(1)
        logger.info("Executando operação...")