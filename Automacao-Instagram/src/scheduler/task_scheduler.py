#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Task Scheduler - Gerenciador de tarefas agendadas
Version: 1.0.0
"""

import schedule
import time
import threading
import queue
import json
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

from src.utils.logger import get_logger

class TaskPriority(Enum):
    """
    Prioridades para tarefas
    """
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class ScheduledTask:
    """
    Estrutura para uma tarefa agendada
    """
    id: str
    name: str
    function: Callable
    schedule_time: str
    days: List[str]
    priority: TaskPriority = TaskPriority.NORMAL
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0
    max_retries: int = 3
    retry_delay: int = 60
    timeout: int = 300
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a tarefa para dicionario
        """
        data = asdict(self)
        data['function'] = self.function.__name__
        data['priority'] = self.priority.value
        data['last_run'] = self.last_run.isoformat() if self.last_run else None
        data['next_run'] = self.next_run.isoformat() if self.next_run else None
        return data

class TaskScheduler:
    """
    Scheduler avancado para tarefas
    """
    
    def __init__(self):
        """
        Inicializa o scheduler
        """
        self.logger = get_logger(__name__)
        self.tasks: Dict[str, ScheduledTask] = {}
        self.task_queue = queue.PriorityQueue()
        self.running = False
        self.thread = None
        self.execution_history = []
        
        # Configuracoes
        self.max_history = 1000
        
        self.logger.info("Task Scheduler inicializado")
    
    def add_task(self, task: ScheduledTask) -> bool:
        """
        Adiciona uma tarefa ao scheduler
        
        Args:
            task: Tarefa a ser adicionada
        
        Returns:
            True se adicionado com sucesso
        """
        if task.id in self.tasks:
            self.logger.warning(f"Tarefa {task.id} ja existe")
            return False
        
        self.tasks[task.id] = task
        self.logger.info(f"Tarefa adicionada: {task.name} (ID: {task.id})")
        return True
    
    def remove_task(self, task_id: str) -> bool:
        """
        Remove uma tarefa do scheduler
        
        Args:
            task_id: ID da tarefa
        
        Returns:
            True se removido com sucesso
        """
        if task_id not in self.tasks:
            self.logger.warning(f"Tarefa {task_id} nao encontrada")
            return False
        
        del self.tasks[task_id]
        self.logger.info(f"Tarefa removida: {task_id}")
        return True
    
    def enable_task(self, task_id: str) -> bool:
        """
        Habilita uma tarefa
        
        Args:
            task_id: ID da tarefa
        
        Returns:
            True se habilitado com sucesso
        """
        if task_id not in self.tasks:
            self.logger.warning(f"Tarefa {task_id} nao encontrada")
            return False
        
        self.tasks[task_id].enabled = True
        self.logger.info(f"Tarefa habilitada: {task_id}")
        return True
    
    def disable_task(self, task_id: str) -> bool:
        """
        Desabilita uma tarefa
        
        Args:
            task_id: ID da tarefa
        
        Returns:
            True se desabilitado com sucesso
        """
        if task_id not in self.tasks:
            self.logger.warning(f"Tarefa {task_id} nao encontrada")
            return False
        
        self.tasks[task_id].enabled = False
        self.logger.info(f"Tarefa desabilitada: {task_id}")
        return True
    
    def start(self):
        """
        Inicia o scheduler
        """
        if self.running:
            self.logger.warning("Scheduler ja esta em execucao")
            return
        
        self.logger.info("Iniciando Task Scheduler...")
        self.running = True
        
        # Configura as tarefas
        self._setup_tasks()
        
        # Inicia a thread principal
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        self.logger.info("Task Scheduler iniciado")
    
    def stop(self):
        """
        Para o scheduler
        """
        self.logger.info("Parando Task Scheduler...")
        self.running = False
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        
        self.logger.info("Task Scheduler parado")
    
    def _setup_tasks(self):
        """
        Configura as tarefas no schedule
        """
        for task_id, task in self.tasks.items():
            if not task.enabled:
                continue
            
            self._schedule_task(task)
    
    def _schedule_task(self, task: ScheduledTask):
        """
        Agenda uma tarefa especifica
        
        Args:
            task: Tarefa a ser agendada
        """
        days_map = {
            'monday': schedule.every().monday,
            'tuesday': schedule.every().tuesday,
            'wednesday': schedule.every().wednesday,
            'thursday': schedule.every().thursday,
            'friday': schedule.every().friday,
            'saturday': schedule.every().saturday,
            'sunday': schedule.every().sunday
        }
        
        if task.days:
            for day in task.days:
                if day in days_map:
                    job = days_map[day].at(task.schedule_time).do(
                        self._execute_task, task_id=task.id
                    )
                    self.logger.debug(f"Tarefa {task.name} agendada para {day} as {task.schedule_time}")
        else:
            job = schedule.every().day.at(task.schedule_time).do(
                self._execute_task, task_id=task.id
            )
            self.logger.debug(f"Tarefa {task.name} agendada para todos os dias as {task.schedule_time}")
    
    def _execute_task(self, task_id: str):
        """
        Executa uma tarefa
        
        Args:
            task_id: ID da tarefa
        """
        if task_id not in self.tasks:
            self.logger.error(f"Tarefa {task_id} nao encontrada")
            return
        
        task = self.tasks[task_id]
        
        if not task.enabled:
            self.logger.debug(f"Tarefa {task.name} desabilitada, ignorando")
            return
        
        self.logger.info(f"Executando tarefa: {task.name}")
        
        # Adiciona a fila de execucao
        self.task_queue.put((task.priority.value, task_id))
        
        # Executa em thread separada
        thread = threading.Thread(
            target=self._run_task,
            args=(task_id,),
            daemon=True
        )
        thread.start()
    
    def _run_task(self, task_id: str):
        """
        Executa uma tarefa com retry e timeout
        
        Args:
            task_id: ID da tarefa
        """
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        
        start_time = datetime.now()
        attempts = 0
        success = False
        
        while attempts < task.max_retries and not success:
            try:
                self.logger.debug(f"Executando {task.name} (tentativa {attempts + 1})")
                
                # Executa a funcao com timeout
                result = self._run_with_timeout(task.function, task.timeout)
                
                success = True
                self.logger.info(f"Tarefa {task.name} executada com sucesso")
                
                # Atualiza estatisticas
                task.last_run = datetime.now()
                task.run_count += 1
                task.next_run = self._calculate_next_run(task)
                
                # Registra no historico
                self._add_history(task_id, True, result)
                
            except TimeoutError:
                error_msg = f"Timeout ao executar {task.name} (limite: {task.timeout}s)"
                self.logger.error(error_msg)
                attempts += 1
                self._add_history(task_id, False, error_msg)
                
            except Exception as e:
                error_msg = f"Erro ao executar {task.name}: {str(e)}"
                self.logger.error(error_msg)
                attempts += 1
                self._add_history(task_id, False, error_msg)
                
            if not success and attempts < task.max_retries:
                self.logger.info(f"Tentando novamente em {task.retry_delay}s...")
                time.sleep(task.retry_delay)
        
        if not success:
            self.logger.error(f"Falha ao executar {task.name} apos {task.max_retries} tentativas")
    
    def _run_with_timeout(self, func: Callable, timeout: int) -> Any:
        """
        Executa uma funcao com timeout
        
        Args:
            func: Funcao a ser executada
            timeout: Timeout em segundos
        
        Returns:
            Resultado da funcao
        """
        result_queue = queue.Queue()
        
        def wrapper():
            try:
                result = func()
                result_queue.put(('success', result))
            except Exception as e:
                result_queue.put(('error', str(e)))
        
        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()
        thread.join(timeout=timeout)
        
        if thread.is_alive():
            raise TimeoutError(f"Funcao excedeu o timeout de {timeout} segundos")
        
        status, result = result_queue.get()
        
        if status == 'error':
            raise Exception(result)
        
        return result
    
    def _calculate_next_run(self, task: ScheduledTask) -> Optional[datetime]:
        """
        Calcula a proxima execucao da tarefa
        
        Args:
            task: Tarefa
        
        Returns:
            Datetime da proxima execucao
        """
        now = datetime.now()
        hour, minute = map(int, task.schedule_time.split(':'))
        
        days_map = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        current_day = now.weekday()
        
        if task.days:
            for day in task.days:
                if day in days_map:
                    target_day = days_map[day]
                    if target_day > current_day:
                        days_until = target_day - current_day
                        next_date = now + timedelta(days=days_until)
                        return next_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            first_day = days_map[task.days[0]]
            days_until = 7 - current_day + first_day
            next_date = now + timedelta(days=days_until)
            return next_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        else:
            next_date = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_date <= now:
                next_date += timedelta(days=1)
            return next_date
    
    def _add_history(self, task_id: str, success: bool, result: Any):
        """
        Adiciona ao historico de execucoes
        
        Args:
            task_id: ID da tarefa
            success: True se bem sucedido
            result: Resultado ou erro
        """
        entry = {
            'task_id': task_id,
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'result': str(result)
        }
        
        self.execution_history.append(entry)
        
        if len(self.execution_history) > self.max_history:
            self.execution_history = self.execution_history[-self.max_history:]
    
    def _run_loop(self):
        """
        Loop principal do scheduler
        """
        self.logger.info("Loop do Task Scheduler iniciado")
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)
            except Exception as e:
                self.logger.error(f"Erro no loop do scheduler: {str(e)}")
                time.sleep(60)
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtem o status de uma tarefa
        
        Args:
            task_id: ID da tarefa
        
        Returns:
            Dict com status
        """
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        return task.to_dict()
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Obtem todas as tarefas
        
        Returns:
            Lista de dicionarios com informacoes das tarefas
        """
        return [task.to_dict() for task in self.tasks.values()]
    
    def get_history(self, task_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtem o historico de execucoes
        
        Args:
            task_id: ID da tarefa (opcional)
            limit: Limite de registros
        
        Returns:
            Lista de entradas do historico
        """
        history = self.execution_history
        
        if task_id:
            history = [h for h in history if h.get('task_id') == task_id]
        
        return history[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtem estatisticas do scheduler
        
        Returns:
            Dict com estatisticas
        """
        total_tasks = len(self.tasks)
        enabled_tasks = len([t for t in self.tasks.values() if t.enabled])
        
        total_executions = len(self.execution_history)
        successful_executions = len([h for h in self.execution_history if h.get('success', False)])
        
        success_rate = (successful_executions / total_executions * 100) if total_executions > 0 else 0
        
        return {
            'total_tasks': total_tasks,
            'enabled_tasks': enabled_tasks,
            'disabled_tasks': total_tasks - enabled_tasks,
            'total_executions': total_executions,
            'successful_executions': successful_executions,
            'failed_executions': total_executions - successful_executions,
            'success_rate': success_rate,
            'queue_size': self.task_queue.qsize(),
            'running': self.running,
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    def test_function():
        print(f"Teste executado em {datetime.now()}")
        return "Sucesso"
    
    scheduler = TaskScheduler()
    
    task = ScheduledTask(
        id="test_1",
        name="Test Task",
        function=test_function,
        schedule_time="08:00",
        days=['monday', 'wednesday', 'friday'],
        priority=TaskPriority.NORMAL
    )
    
    scheduler.add_task(task)
    print("Task adicionada com sucesso!")
    print(f"Status: {scheduler.get_task_status('test_1')}")
    
    scheduler.start()
    
    try:
        while True:
            time.sleep(10)
            stats = scheduler.get_statistics()
            print(f"Estatisticas: {json.dumps(stats, indent=2)}")
    except KeyboardInterrupt:
        scheduler.stop()
        print("Scheduler parado")
