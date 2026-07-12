#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Scheduler Manager - Gerenciador de agendamentos
Version: 1.0.0
"""

import schedule
import time
import threading
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

from src.utils.logger import get_logger
from src.api.instagram_publisher import InstagramPublisher

class SchedulerManager:
    """
    Gerenciador de agendamentos para publicações
    """
    
    def __init__(self, publisher: InstagramPublisher, config: Dict[str, Any]):
        """
        Inicializa o gerenciador
        
        Args:
            publisher: Instância do publicador
            config: Configurações do sistema
        """
        self.logger = get_logger(__name__)
        self.publisher = publisher
        self.config = config
        self.jobs = []
        self.running = False
        self.thread = None
        
        # Configurações de agendamento
        scheduling_config = config.get('scheduling', {})
        self.post_time = scheduling_config.get('posts', {}).get('time', '08:00')
        self.story_time = scheduling_config.get('stories', {}).get('time', '18:00')
        self.post_days = scheduling_config.get('posts', {}).get('days', [])
        self.story_days = scheduling_config.get('stories', {}).get('days', [])
        self.post_delay = scheduling_config.get('posts', {}).get('random_delay_minutes', 10)
        self.story_delay = scheduling_config.get('stories', {}).get('random_delay_minutes', 5)
        
        # Carrega histórico
        self.load_history()
        
        self.logger.info(f"Scheduler Manager inicializado")
        self.logger.info(f"Posts agendados para: {self.post_time}")
        self.logger.info(f"Stories agendados para: {self.story_time}")
    
    def setup_schedule(self):
        """
        Configura os agendamentos
        """
        self.logger.info("Configurando agendamentos...")
        
        # Limpa agendamentos anteriores
        schedule.clear()
        
        # Agendamento de posts
        if self.config.get('scheduling', {}).get('posts', {}).get('enabled', True):
            self._schedule_posts()
        
        # Agendamento de stories
        if self.config.get('scheduling', {}).get('stories', {}).get('enabled', True):
            self._schedule_stories()
        
        self.logger.info("Agendamentos configurados com sucesso")
    
    def _schedule_posts(self):
        """
        Configura o agendamento de posts
        """
        self.logger.info(f"Configurando posts para {self.post_time}")
        
        # Converte o horário
        hour, minute = map(int, self.post_time.split(':'))
        
        # Agenda para cada dia da semana
        days_map = {
            'monday': schedule.every().monday,
            'tuesday': schedule.every().tuesday,
            'wednesday': schedule.every().wednesday,
            'thursday': schedule.every().thursday,
            'friday': schedule.every().friday,
            'saturday': schedule.every().saturday,
            'sunday': schedule.every().sunday
        }
        
        if self.post_days:
            for day in self.post_days:
                if day in days_map:
                    job = days_map[day].at(self.post_time).do(self._publish_daily_posts)
                    self.jobs.append(job)
                    self.logger.info(f"Post agendado para {day} às {self.post_time}")
        else:
            # Todos os dias
            job = schedule.every().day.at(self.post_time).do(self._publish_daily_posts)
            self.jobs.append(job)
            self.logger.info(f"Post agendado para todos os dias às {self.post_time}")
    
    def _schedule_stories(self):
        """
        Configura o agendamento de stories
        """
        self.logger.info(f"Configurando stories para {self.story_time}")
        
        # Converte o horário
        hour, minute = map(int, self.story_time.split(':'))
        
        # Agenda para cada dia da semana
        days_map = {
            'monday': schedule.every().monday,
            'tuesday': schedule.every().tuesday,
            'wednesday': schedule.every().wednesday,
            'thursday': schedule.every().thursday,
            'friday': schedule.every().friday,
            'saturday': schedule.every().saturday,
            'sunday': schedule.every().sunday
        }
        
        if self.story_days:
            for day in self.story_days:
                if day in days_map:
                    job = days_map[day].at(self.story_time).do(self._publish_daily_stories)
                    self.jobs.append(job)
                    self.logger.info(f"Story agendado para {day} às {self.story_time}")
        else:
            # Todos os dias
            job = schedule.every().day.at(self.story_time).do(self._publish_daily_stories)
            self.jobs.append(job)
            self.logger.info(f"Story agendado para todos os dias às {self.story_time}")
    
    def _publish_daily_posts(self):
        """
        Executa a publicação diária de posts
        """
        self.logger.info(f"Executando publicação diária de posts - {datetime.now()}")
        
        try:
            # Adiciona um pequeno delay aleatório
            if self.post_delay > 0:
                delay = self.post_delay * 60 * 0.3  # 30% do delay máximo
                time.sleep(delay)
            
            result = self.publisher.publish_daily_posts()
            
            if result.get('success'):
                self.logger.info(f"Post publicado com sucesso: {result.get('media_id')}")
            else:
                self.logger.error(f"Falha ao publicar post: {result.get('error')}")
            
            # Salva histórico após cada execução
            self.publisher._save_history()
            self.save_history()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro na publicação diária de posts: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _publish_daily_stories(self):
        """
        Executa a publicação diária de stories
        """
        self.logger.info(f"Executando publicação diária de stories - {datetime.now()}")
        
        try:
            # Adiciona um pequeno delay aleatório
            if self.story_delay > 0:
                delay = self.story_delay * 60 * 0.3  # 30% do delay máximo
                time.sleep(delay)
            
            result = self.publisher.publish_daily_stories()
            
            if result.get('success'):
                self.logger.info(f"Story publicado com sucesso: {result.get('story_id')}")
            else:
                self.logger.error(f"Falha ao publicar story: {result.get('error')}")
            
            # Salva histórico após cada execução
            self.publisher._save_history()
            self.save_history()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro na publicação diária de stories: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def run_pending_tasks(self):
        """
        Executa todas as tarefas pendentes
        """
        try:
            schedule.run_pending()
        except Exception as e:
            self.logger.error(f"Erro ao executar tarefas pendentes: {str(e)}")
    
    def start(self):
        """
        Inicia o scheduler em uma thread separada
        """
        if self.running:
            self.logger.warning("Scheduler já está em execução")
            return
        
        self.logger.info("Iniciando scheduler...")
        self.setup_schedule()
        self.running = True
        
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        self.logger.info("Scheduler iniciado com sucesso")
    
    def _run_loop(self):
        """
        Loop principal do scheduler
        """
        self.logger.info("Loop do scheduler iniciado")
        
        while self.running:
            try:
                self.run_pending_tasks()
                time.sleep(60)  # Verifica a cada minuto
            except Exception as e:
                self.logger.error(f"Erro no loop do scheduler: {str(e)}")
                time.sleep(60)
    
    def stop(self):
        """
        Para o scheduler
        """
        self.logger.info("Parando scheduler...")
        self.running = False
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        
        self.logger.info("Scheduler parado")
    
    def get_post_schedule(self) -> str:
        """
        Retorna o horário agendado para posts
        
        Returns:
            String com o horário
        """
        return self.post_time
    
    def get_story_schedule(self) -> str:
        """
        Retorna o horário agendado para stories
        
        Returns:
            String com o horário
        """
        return self.story_time
    
    def should_run_immediately(self) -> bool:
        """
        Verifica se deve executar tarefas imediatamente
        
        Returns:
            True se deve executar imediatamente
        """
        # Verifica se há tarefas pendentes que deveriam ter sido executadas
        current_time = datetime.now()
        last_execution = self.get_last_execution()
        
        if not last_execution:
            return True
        
        # Se a última execução foi há mais de 24 horas, executa
        if (current_time - last_execution) > timedelta(days=1):
            return True
        
        return False
    
    def get_last_execution(self) -> Optional[datetime]:
        """
        Obtém a última execução do histórico
        
        Returns:
            Datetime da última execução ou None
        """
        history = self.publisher.publication_history
        
        if not history:
            return None
        
        # Obtém a data da última publicação
        last_entry = history[-1]
        timestamp = last_entry.get('timestamp')
        
        if timestamp:
            try:
                return datetime.fromisoformat(timestamp)
            except:
                pass
        
        return None
    
    def save_history(self):
        """
        Salva o histórico do scheduler
        """
        try:
            history_file = './logs/scheduler_history.json'
            os.makedirs(os.path.dirname(history_file), exist_ok=True)
            
            history_data = {
                'post_schedule': self.post_time,
                'story_schedule': self.story_time,
                'last_execution': datetime.now().isoformat(),
                'jobs_count': len(self.jobs),
                'timestamp': datetime.now().isoformat()
            }
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
            
            self.logger.debug("Histórico do scheduler salvo")
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar histórico do scheduler: {str(e)}")
    
    def load_history(self):
        """
        Carrega o histórico do scheduler
        """
        try:
            history_file = './logs/scheduler_history.json'
            
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                self.logger.info(f"Histórico do scheduler carregado: {history_data}")
            else:
                self.logger.info("Nenhum histórico do scheduler encontrado")
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar histórico do scheduler: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtém o status do scheduler
        
        Returns:
            Dict com status
        """
        return {
            'running': self.running,
            'jobs': len(self.jobs),
            'post_schedule': self.post_time,
            'story_schedule': self.story_time,
            'last_execution': self.get_last_execution(),
            'timestamp': datetime.now().isoformat()
        }

# Para testes
if __name__ == "__main__":
    from src.api.instagram_publisher import InstagramPublisher
    
    publisher = InstagramPublisher()
    scheduler = SchedulerManager(publisher, {
        'scheduling': {
            'posts': {'enabled': True, 'time': '08:00', 'days': []},
            'stories': {'enabled': True, 'time': '18:00', 'days': []}
        }
    })
    
    print("Scheduler instanciado com sucesso!")
    scheduler.start()
    
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.stop()
        print("Scheduler parado")