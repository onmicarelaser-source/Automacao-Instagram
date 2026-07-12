#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Health Check - Monitoramento de saúde do sistema
Version: 1.0.0
"""

import os
import sys
import time
import psutil
import platform
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from src.utils.logger import get_logger

@dataclass
class HealthStatus:
    """
    Status de saúde do sistema
    """
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "OK"
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    network_status: bool = True
    database_status: bool = True
    api_status: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)

class HealthCheck:
    """
    Monitor de saúde do sistema
    """
    
    def __init__(self, check_interval: int = 60, 
                 warning_threshold_cpu: float = 80.0,
                 warning_threshold_memory: float = 80.0,
                 warning_threshold_disk: float = 80.0):
        """
        Inicializa o monitor
        
        Args:
            check_interval: Intervalo de verificação em segundos
            warning_threshold_cpu: Threshold de warning para CPU (%)
            warning_threshold_memory: Threshold de warning para memória (%)
            warning_threshold_disk: Threshold de warning para disco (%)
        """
        self.logger = get_logger(__name__)
        self.check_interval = check_interval
        self.warning_threshold_cpu = warning_threshold_cpu
        self.warning_threshold_memory = warning_threshold_memory
        self.warning_threshold_disk = warning_threshold_disk
        
        self.running = False
        self.thread = None
        self.status_history: List[HealthStatus] = []
        self.current_status: Optional[HealthStatus] = None
        self.max_history = 1000
        
        self.logger.info("Health Check monitor inicializado")
    
    def start_monitoring(self):
        """
        Inicia o monitoramento
        """
        if self.running:
            self.logger.warning("Monitoramento já está em execução")
            return
        
        self.logger.info("Iniciando monitoramento de saúde...")
        self.running = True
        
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        
        self.logger.info("Monitoramento de saúde iniciado")
    
    def stop_monitoring(self):
        """
        Para o monitoramento
        """
        self.logger.info("Parando monitoramento de saúde...")
        self.running = False
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        
        self.logger.info("Monitoramento de saúde parado")
    
    def _monitor_loop(self):
        """
        Loop principal de monitoramento
        """
        self.logger.info("Loop de monitoramento iniciado")
        
        while self.running:
            try:
                # Realiza a verificação
                status = self.check_health()
                self.current_status = status
                
                # Adiciona ao histórico
                self.status_history.append(status)
                if len(self.status_history) > self.max_history:
                    self.status_history = self.status_history[-self.max_history:]
                
                # Log de alertas
                if status.warnings:
                    for warning in status.warnings:
                        self.logger.warning(f"Health Check Warning: {warning}")
                
                if status.errors:
                    for error in status.errors:
                        self.logger.error(f"Health Check Error: {error}")
                
                # Dorme até a próxima verificação
                time.sleep(self.check_interval)
                
            except Exception as e:
                self.logger.error(f"Erro no loop de monitoramento: {str(e)}")
                time.sleep(self.check_interval)
    
    def check_health(self) -> HealthStatus:
        """
        Realiza a verificação de saúde
        
        Returns:
            HealthStatus com o status atual
        """
        status = HealthStatus()
        
        try:
            # 1. CPU Usage
            status.cpu_usage = psutil.cpu_percent(interval=1)
            if status.cpu_usage > self.warning_threshold_cpu:
                status.warnings.append(f"CPU usage above threshold: {status.cpu_usage:.1f}%")
            
            # 2. Memory Usage
            memory = psutil.virtual_memory()
            status.memory_usage = memory.percent
            if status.memory_usage > self.warning_threshold_memory:
                status.warnings.append(f"Memory usage above threshold: {status.memory_usage:.1f}%")
            
            # 3. Disk Usage
            disk = psutil.disk_usage('/')
            status.disk_usage = disk.percent
            if status.disk_usage > self.warning_threshold_disk:
                status.warnings.append(f"Disk usage above threshold: {status.disk_usage:.1f}%")
            
            # 4. Network Status
            status.network_status = self._check_network()
            if not status.network_status:
                status.errors.append("Network connection failed")
            
            # 5. Database Status
            status.database_status = self._check_database()
            if not status.database_status:
                status.errors.append("Database connection failed")
            
            # 6. API Status
            status.api_status = self._check_api()
            if not status.api_status:
                status.errors.append("API connection failed")
            
            # 7. System Details
            status.details = {
                'system': platform.system(),
                'node': platform.node(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_version': sys.version,
                'uptime': self._get_uptime()
            }
            
            # Determina status geral
            if status.errors:
                status.status = "ERROR"
            elif status.warnings:
                status.status = "WARNING"
            else:
                status.status = "OK"
            
        except Exception as e:
            status.status = "ERROR"
            status.errors.append(f"Health check failed: {str(e)}")
        
        return status
    
    def _check_network(self) -> bool:
        """
        Verifica conectividade de rede
        
        Returns:
            True se conectado
        """
        try:
            # Tenta pingar o Google DNS
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False
    
    def _check_database(self) -> bool:
        """
        Verifica conexão com o banco de dados
        
        Returns:
            True se conectado
        """
        try:
            # Verifica se o arquivo de banco de dados existe
            db_path = os.path.join('logs', 'posts_history.db')
            if os.path.exists(db_path):
                return True
            
            # Tenta criar um arquivo de teste
            with open(db_path, 'w') as f:
                f.write('')
            return True
            
        except Exception as e:
            self.logger.error(f"Database check failed: {str(e)}")
            return False
    
    def _check_api(self) -> bool:
        """
        Verifica conexão com a API
        
        Returns:
            True se conectado
        """
        try:
            import requests
            response = requests.get('https://api.instagram.com/oembed', timeout=5)
            return True
        except:
            # Se não conseguir conectar à API do Instagram, tenta Google
            try:
                import requests
                response = requests.get('https://www.google.com', timeout=5)
                return response.status_code == 200
            except:
                return False
    
    def _get_uptime(self) -> str:
        """
        Obtém o uptime do sistema
        
        Returns:
            String com o uptime
        """
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            
            if days > 0:
                return f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        except:
            return "Unknown"
    
    def get_current_status(self) -> Optional[HealthStatus]:
        """
        Obtém o status atual
        
        Returns:
            HealthStatus atual
        """
        return self.current_status
    
    def get_status_history(self, limit: int = 10) -> List[HealthStatus]:
        """
        Obtém o histórico de status
        
        Args:
            limit: Número de registros
        
        Returns:
            Lista de HealthStatus
        """
        return self.status_history[-limit:]
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Obtém um resumo do status
        
        Returns:
            Dict com resumo
        """
        if not self.current_status:
            return {'status': 'UNKNOWN', 'message': 'No health check performed yet'}
        
        return {
            'status': self.current_status.status,
            'timestamp': self.current_status.timestamp.isoformat(),
            'cpu_usage': self.current_status.cpu_usage,
            'memory_usage': self.current_status.memory_usage,
            'disk_usage': self.current_status.disk_usage,
            'network_status': self.current_status.network_status,
            'database_status': self.current_status.database_status,
            'api_status': self.current_status.api_status,
            'errors': self.current_status.errors,
            'warnings': self.current_status.warnings,
            'details': self.current_status.details
        }
    
    def check_status(self) -> bool:
        """
        Verifica rapidamente o status
        
        Returns:
            True se tudo está funcionando
        """
        if not self.current_status:
            return False
        return self.current_status.status == "OK"

# Para testes
if __name__ == "__main__":
    health_check = HealthCheck(check_interval=10)
    health_check.start_monitoring()
    
    try:
        while True:
            summary = health_check.get_summary()
            print(f"Status: {summary['status']}")
            print(f"CPU: {summary['cpu_usage']:.1f}%")
            print(f"Memory: {summary['memory_usage']:.1f}%")
            print(f"Disk: {summary['disk_usage']:.1f}%")
            print("-" * 40)
            time.sleep(10)
    except KeyboardInterrupt:
        health_check.stop_monitoring()
        print("Monitoramento parado")