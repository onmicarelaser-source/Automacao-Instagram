#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for Scheduler Manager
Version: 1.0.0
"""

import unittest
import os
import json
import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.scheduler.scheduler_manager import SchedulerManager
from src.api.instagram_publisher import InstagramPublisher
from src.utils.logger import setup_logger

class TestSchedulerManager(unittest.TestCase):
    """
    Testes para o Scheduler Manager
    """
    
    def setUp(self):
        """
        Configuração dos testes
        """
        # Configura logger
        self.logger = setup_logger(
            log_level="DEBUG",
            log_file="./logs/test.log",
            console_output=True
        )
        
        # Mock do publisher
        self.publisher = Mock(spec=InstagramPublisher)
        self.publisher.publication_history = []
        self.publisher.failed_posts = []
        
        # Configuração
        self.config = {
            'scheduling': {
                'posts': {
                    'enabled': True,
                    'time': '08:00',
                    'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
                    'random_delay_minutes': 10
                },
                'stories': {
                    'enabled': True,
                    'time': '18:00',
                    'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
                    'random_delay_minutes': 5
                }
            }
        }
        
        # Cria o scheduler
        self.scheduler = SchedulerManager(self.publisher, self.config)
    
    def test_scheduler_initialization(self):
        """
        Testa a inicialização do scheduler
        """
        self.assertIsNotNone(self.scheduler)
        self.assertEqual(self.scheduler.post_time, '08:00')
        self.assertEqual(self.scheduler.story_time, '18:00')
        self.assertEqual(len(self.scheduler.post_days), 5)
        self.assertEqual(len(self.scheduler.story_days), 5)
    
    def test_setup_schedule(self):
        """
        Testa a configuração do agendamento
        """
        self.scheduler.setup_schedule()
        
        # Verifica que jobs foram criados
        self.assertGreater(len(self.scheduler.jobs), 0)
    
    def test_get_post_schedule(self):
        """
        Testa a obtenção do horário de posts
        """
        schedule = self.scheduler.get_post_schedule()
        self.assertEqual(schedule, '08:00')
    
    def test_get_story_schedule(self):
        """
        Testa a obtenção do horário de stories
        """
        schedule = self.scheduler.get_story_schedule()
        self.assertEqual(schedule, '18:00')
    
    def test_should_run_immediately(self):
        """
        Testa a verificação de execução imediata
        """
        # Sem histórico - deve executar
        self.assertTrue(self.scheduler.should_run_immediately())
        
        # Com histórico recente - não deve executar
        self.publisher.publication_history = [{
            'timestamp': datetime.now().isoformat()
        }]
        self.assertFalse(self.scheduler.should_run_immediately())
        
        # Com histórico antigo - deve executar
        old_date = datetime.now() - timedelta(days=2)
        self.publisher.publication_history = [{
            'timestamp': old_date.isoformat()
        }]
        self.assertTrue(self.scheduler.should_run_immediately())
    
    def test_get_last_execution(self):
        """
        Testa a obtenção da última execução
        """
        # Sem histórico
        self.assertIsNone(self.scheduler.get_last_execution())
        
        # Com histórico
        test_date = datetime.now()
        self.publisher.publication_history = [{
            'timestamp': test_date.isoformat()
        }]
        
        last_execution = self.scheduler.get_last_execution()
        self.assertIsNotNone(last_execution)
        self.assertEqual(last_execution.date(), test_date.date())
    
    def test_save_and_load_history(self):
        """
        Testa o salvamento e carregamento do histórico
        """
        # Salva
        self.scheduler.save_history()
        
        # Carrega
        self.scheduler.load_history()
        
        # Verifica (não deve lançar exceção)
        self.assertTrue(True)
    
    def test_get_status(self):
        """
        Testa a obtenção do status
        """
        status = self.scheduler.get_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn('running', status)
        self.assertIn('jobs', status)
        self.assertIn('post_schedule', status)
        self.assertIn('story_schedule', status)
        self.assertIn('timestamp', status)
    
    def test_start_and_stop(self):
        """
        Testa o início e parada do scheduler
        """
        # Inicia
        self.scheduler.start()
        self.assertTrue(self.scheduler.running)
        
        # Espera um pouco
        time.sleep(1)
        
        # Para
        self.scheduler.stop()
        self.assertFalse(self.scheduler.running)
    
    def test_publish_daily_posts(self):
        """
        Testa a publicação diária de posts
        """
        # Mock da publicação
        self.publisher.publish_daily_posts.return_value = {
            'success': True,
            'media_id': '123456'
        }
        
        # Executa
        result = self.scheduler._publish_daily_posts()
        
        # Verifica
        self.assertTrue(result.get('success', False))
        self.publisher.publish_daily_posts.assert_called_once()
    
    def test_publish_daily_stories(self):
        """
        Testa a publicação diária de stories
        """
        # Mock da publicação
        self.publisher.publish_daily_stories.return_value = {
            'success': True,
            'story_id': '789012'
        }
        
        # Executa
        result = self.scheduler._publish_daily_stories()
        
        # Verifica
        self.assertTrue(result.get('success', False))
        self.publisher.publish_daily_stories.assert_called_once()
    
    def test_scheduler_with_no_days(self):
        """
        Testa o scheduler sem dias especificados
        """
        # Configuração sem dias
        config = {
            'scheduling': {
                'posts': {
                    'enabled': True,
                    'time': '08:00',
                    'days': [],
                    'random_delay_minutes': 10
                },
                'stories': {
                    'enabled': True,
                    'time': '18:00',
                    'days': [],
                    'random_delay_minutes': 5
                }
            }
        }
        
        scheduler = SchedulerManager(self.publisher, config)
        scheduler.setup_schedule()
        
        # Deve ter criado jobs
        self.assertGreater(len(scheduler.jobs), 0)
    
    def test_scheduler_disabled_posts(self):
        """
        Testa o scheduler com posts desabilitados
        """
        # Configuração com posts desabilitados
        config = {
            'scheduling': {
                'posts': {
                    'enabled': False,
                    'time': '08:00',
                    'days': ['monday'],
                    'random_delay_minutes': 10
                },
                'stories': {
                    'enabled': True,
                    'time': '18:00',
                    'days': ['monday'],
                    'random_delay_minutes': 5
                }
            }
        }
        
        scheduler = SchedulerManager(self.publisher, config)
        scheduler.setup_schedule()
        
        # Deve ter apenas stories
        self.assertEqual(len(scheduler.jobs), 1)
    
    def test_scheduler_disabled_stories(self):
        """
        Testa o scheduler com stories desabilitados
        """
        # Configuração com stories desabilitados
        config = {
            'scheduling': {
                'posts': {
                    'enabled': True,
                    'time': '08:00',
                    'days': ['monday'],
                    'random_delay_minutes': 10
                },
                'stories': {
                    'enabled': False,
                    'time': '18:00',
                    'days': ['monday'],
                    'random_delay_minutes': 5
                }
            }
        }
        
        scheduler = SchedulerManager(self.publisher, config)
        scheduler.setup_schedule()
        
        # Deve ter apenas posts
        self.assertEqual(len(scheduler.jobs), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)