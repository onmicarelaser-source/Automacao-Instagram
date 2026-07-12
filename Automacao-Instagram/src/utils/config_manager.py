#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Config Manager - Gerenciamento de configurações
Version: 1.0.0
"""

import os
import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

from src.utils.logger import get_logger

class ConfigManager:
    """
    Gerenciador de configurações
    """
    
    def __init__(self, config_path: str = "./config/config.json"):
        """
        Inicializa o gerenciador
        
        Args:
            config_path: Caminho do arquivo de configuração
        """
        self.logger = get_logger(__name__)
        self.config_path = config_path
        self.config = {}
        self.env_loaded = False
        
        # Carrega variáveis de ambiente
        self._load_env()
        
        # Carrega configuração
        self.load_config()
    
    def _load_env(self):
        """
        Carrega variáveis de ambiente do arquivo .env
        """
        env_file = os.path.join(os.path.dirname(os.path.dirname(self.config_path)), '.env')
        
        if os.path.exists(env_file):
            load_dotenv(env_file)
            self.logger.info(f"Arquivo .env carregado: {env_file}")
            self.env_loaded = True
        else:
            self.logger.warning(f"Arquivo .env não encontrado: {env_file}")
    
    def load_config(self) -> Dict[str, Any]:
        """
        Carrega a configuração do arquivo
        
        Returns:
            Dict com a configuração
        """
        if not os.path.exists(self.config_path):
            self.logger.warning(f"Arquivo de configuração não encontrado: {self.config_path}")
            
            # Tenta carregar como JSON
            config_dir = os.path.dirname(self.config_path)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
            
            # Cria configuração padrão
            self.config = self._create_default_config()
            self.save_config()
            self.logger.info("Configuração padrão criada")
        else:
            try:
                # Tenta carregar como JSON
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self.logger.info(f"Configuração carregada de: {self.config_path}")
                
            except json.JSONDecodeError:
                # Tenta carregar como YAML
                try:
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        self.config = yaml.safe_load(f)
                    self.logger.info(f"Configuração YAML carregada de: {self.config_path}")
                except Exception as e:
                    self.logger.error(f"Erro ao carregar configuração: {str(e)}")
                    self.config = self._create_default_config()
        
        # Substitui valores de variáveis de ambiente
        self._apply_env_overrides()
        
        return self.config
    
    def _apply_env_overrides(self):
        """
        Aplica overrides de variáveis de ambiente
        """
        env_mappings = {
            'APP_NAME': ('application', 'name'),
            'DEBUG': ('application', 'debug'),
            'LOG_LEVEL': ('logging', 'level'),
            'LOG_RETENTION_DAYS': ('logging', 'retention_days'),
            'POST_TIME': ('scheduling', 'posts', 'time'),
            'STORY_TIME': ('scheduling', 'stories', 'time'),
        }
        
        for env_var, path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                self._set_nested_value(self.config, path, value)
                self.logger.debug(f"Override aplicado: {env_var}={value}")
    
    def _set_nested_value(self, config: Dict, path: tuple, value: Any):
        """
        Define um valor em um dicionário aninhado
        
        Args:
            config: Dicionário de configuração
            path: Tupla com o caminho
            value: Valor a ser definido
        """
        current = config
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[path[-1]] = value
    
    def _create_default_config(self) -> Dict[str, Any]:
        """
        Cria uma configuração padrão
        
        Returns:
            Dict com configuração padrão
        """
        return {
            'application': {
                'name': 'Instagram Automation',
                'version': '1.0.0',
                'description': 'Automação de posts e stories para Instagram',
                'debug': False,
                'timezone': 'America/Sao_Paulo'
            },
            'scheduling': {
                'posts': {
                    'enabled': True,
                    'time': '08:00',
                    'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                    'random_delay_minutes': 10
                },
                'stories': {
                    'enabled': True,
                    'time': '18:00',
                    'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                    'random_delay_minutes': 5
                }
            },
            'content': {
                'posts_directory': './assets/posts',
                'stories_directory': './assets/stories',
                'supported_formats': ['.jpg', '.jpeg', '.png', '.mp4'],
                'max_file_size_mb': 100
            },
            'instagram': {
                'api_version': 'v19.0',
                'max_retries': 3,
                'retry_delay_seconds': 60,
                'timeout_seconds': 30
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file': './logs/automation.log',
                'retention_days': 30,
                'max_file_size_mb': 100,
                'backup_count': 5
            },
            'database': {
                'type': 'sqlite',
                'path': './logs/posts_history.db'
            },
            'notifications': {
                'enabled': False,
                'email': {
                    'smtp_server': 'smtp.gmail.com',
                    'smtp_port': 587,
                    'sender': 'automation@seuemail.com',
                    'recipient': 'admin@seuemail.com'
                }
            },
            'backup': {
                'enabled': True,
                'path': './backups',
                'frequency_days': 7,
                'max_backups': 10
            }
        }
    
    def save_config(self):
        """
        Salva a configuração atual
        """
        try:
            # Cria o diretório se não existir
            config_dir = os.path.dirname(self.config_path)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
            
            # Salva como JSON
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Configuração salva em: {self.config_path}")
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar configuração: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém um valor da configuração usando notação de ponto
        
        Args:
            key: Chave usando notação de ponto (ex: 'scheduling.posts.time')
            default: Valor padrão se não encontrado
        
        Returns:
            Valor da configuração
        """
        try:
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
            
        except Exception as e:
            self.logger.debug(f"Erro ao obter {key}: {str(e)}")
            return default
    
    def set(self, key: str, value: Any):
        """
        Define um valor na configuração
        
        Args:
            key: Chave usando notação de ponto
            value: Valor a ser definido
        """
        try:
            keys = key.split('.')
            current = self.config
            
            for k in keys[:-1]:
                if k not in current or not isinstance(current[k], dict):
                    current[k] = {}
                current = current[k]
            
            current[keys[-1]] = value
            self.logger.debug(f"Configuração atualizada: {key}={value}")
            
        except Exception as e:
            self.logger.error(f"Erro ao definir {key}: {str(e)}")
    
    def get_all(self) -> Dict[str, Any]:
        """
        Obtém toda a configuração
        
        Returns:
            Dict com toda a configuração
        """
        return self.config.copy()
    
    def reload(self):
        """
        Recarrega a configuração
        """
        self.logger.info("Recarregando configuração...")
        self.load_config()
        self.logger.info("Configuração recarregada")

# Para testes
if __name__ == "__main__":
    config_manager = ConfigManager()
    print(f"Configuração carregada: {json.dumps(config_manager.get_all(), indent=2)}")
    
    # Testa get
    post_time = config_manager.get('scheduling.posts.time')
    print(f"Horário dos posts: {post_time}")
    
    # Testa set
    config_manager.set('scheduling.posts.time', '09:00')
    print(f"Novo horário: {config_manager.get('scheduling.posts.time')}")