#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Instagram API Client - Cliente para interação com a API do Instagram
Version: 1.0.0
"""

import os
import time
import json
import hashlib
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from urllib.parse import urlencode

from src.utils.logger import get_logger
from src.utils.config_manager import ConfigManager

class InstagramClient:
    """
    Cliente para a API do Instagram Graph
    """
    
    def __init__(self, config_path: str = "./config/config.json"):
        """
        Inicializa o cliente Instagram
        
        Args:
            config_path: Caminho para o arquivo de configuração
        """
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load_config()
        
        # Configurações da API
        self.api_version = self.config.get('instagram', {}).get('api_version', 'v19.0')
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.max_retries = self.config.get('instagram', {}).get('max_retries', 3)
        self.retry_delay = self.config.get('instagram', {}).get('retry_delay_seconds', 60)
        self.timeout = self.config.get('instagram', {}).get('timeout_seconds', 30)
        
        # Credenciais
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
        
        if not self.access_token or not self.account_id:
            self.logger.error("Credenciais do Instagram não encontradas")
            raise ValueError("FACEBOOK_ACCESS_TOKEN e INSTAGRAM_ACCOUNT_ID são obrigatórios")
        
        self.logger.info(f"Instagram Client inicializado (API {self.api_version})")
    
    def publish_post(self, image_path: str, caption: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Publica um post no Instagram
        
        Args:
            image_path: Caminho da imagem
            caption: Legenda do post
            location_id: ID da localização (opcional)
        
        Returns:
            Dict com o resultado da publicação
        """
        self.logger.info(f"Publicando post: {image_path}")
        
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {image_path}")
            
            # Verifica o tamanho do arquivo
            file_size = os.path.getsize(image_path) / (1024 * 1024)  # Em MB
            max_size = self.config.get('content', {}).get('max_file_size_mb', 100)
            
            if file_size > max_size:
                raise ValueError(f"Arquivo muito grande: {file_size:.2f}MB (max: {max_size}MB)")
            
            # 1. Upload da imagem para o servidor do Instagram
            upload_url = f"{self.base_url}/{self.account_id}/media"
            
            with open(image_path, 'rb') as image_file:
                files = {
                    'image': (os.path.basename(image_path), image_file, 'image/jpeg')
                }
                data = {
                    'access_token': self.access_token,
                    'caption': caption,
                    'media_type': 'IMAGE'
                }
                
                if location_id:
                    data['location_id'] = location_id
                
                response = self._make_request('POST', upload_url, data=data, files=files)
            
            # 2. Obtém o ID da criação
            creation_id = response.get('id')
            if not creation_id:
                raise ValueError("ID da criação não retornado")
            
            self.logger.info(f"Upload realizado. ID: {creation_id}")
            
            # 3. Publica o conteúdo
            publish_url = f"{self.base_url}/{self.account_id}/media_publish"
            publish_data = {
                'access_token': self.access_token,
                'creation_id': creation_id
            }
            
            publish_response = self._make_request('POST', publish_url, data=publish_data)
            
            result = {
                'success': True,
                'media_id': publish_response.get('id'),
                'creation_id': creation_id,
                'timestamp': datetime.now().isoformat(),
                'caption': caption
            }
            
            self.logger.info(f"Post publicado com sucesso. ID: {result['media_id']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao publicar post: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def publish_story(self, image_path: str, duration: int = 15) -> Dict[str, Any]:
        """
        Publica um story no Instagram
        
        Args:
            image_path: Caminho da imagem do story
            duration: Duração em segundos
        
        Returns:
            Dict com o resultado da publicação
        """
        self.logger.info(f"Publicando story: {image_path}")
        
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {image_path}")
            
            # 1. Upload da imagem do story
            upload_url = f"{self.base_url}/{self.account_id}/media"
            
            with open(image_path, 'rb') as image_file:
                files = {
                    'image': (os.path.basename(image_path), image_file, 'image/jpeg')
                }
                data = {
                    'access_token': self.access_token,
                    'media_type': 'STORIES',
                    'duration': duration
                }
                
                response = self._make_request('POST', upload_url, data=data, files=files)
            
            # 2. Obtém o ID da criação
            creation_id = response.get('id')
            if not creation_id:
                raise ValueError("ID da criação não retornado")
            
            self.logger.info(f"Upload do story realizado. ID: {creation_id}")
            
            # 3. Publica o story
            publish_url = f"{self.base_url}/{self.account_id}/media_publish"
            publish_data = {
                'access_token': self.access_token,
                'creation_id': creation_id
            }
            
            publish_response = self._make_request('POST', publish_url, data=publish_data)
            
            result = {
                'success': True,
                'story_id': publish_response.get('id'),
                'creation_id': creation_id,
                'duration': duration,
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Story publicado com sucesso. ID: {result['story_id']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao publicar story: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def publish_carousel(self, image_paths: List[str], caption: str) -> Dict[str, Any]:
        """
        Publica um carrossel de posts
        
        Args:
            image_paths: Lista de caminhos das imagens
            caption: Legenda do post
        
        Returns:
            Dict com o resultado da publicação
        """
        self.logger.info(f"Publicando carrossel com {len(image_paths)} imagens")
        
        try:
            # 1. Faz upload de todas as imagens
            children_ids = []
            for path in image_paths:
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Arquivo não encontrado: {path}")
                
                upload_url = f"{self.base_url}/{self.account_id}/media"
                
                with open(path, 'rb') as image_file:
                    files = {
                        'image': (os.path.basename(path), image_file, 'image/jpeg')
                    }
                    data = {
                        'access_token': self.access_token,
                        'is_carousel_item': True
                    }
                    
                    response = self._make_request('POST', upload_url, data=data, files=files)
                    children_ids.append(response.get('id'))
            
            # 2. Cria o carrossel
            carousel_url = f"{self.base_url}/{self.account_id}/media"
            carousel_data = {
                'access_token': self.access_token,
                'media_type': 'CAROUSEL',
                'caption': caption,
                'children': ','.join(children_ids)
            }
            
            carousel_response = self._make_request('POST', carousel_url, data=carousel_data)
            carousel_id = carousel_response.get('id')
            
            # 3. Publica o carrossel
            publish_url = f"{self.base_url}/{self.account_id}/media_publish"
            publish_data = {
                'access_token': self.access_token,
                'creation_id': carousel_id
            }
            
            publish_response = self._make_request('POST', publish_url, data=publish_data)
            
            result = {
                'success': True,
                'carousel_id': publish_response.get('id'),
                'children_count': len(children_ids),
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Carrossel publicado com sucesso. ID: {result['carousel_id']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao publicar carrossel: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_media_status(self, media_id: str) -> Dict[str, Any]:
        """
        Obtém o status de uma mídia publicada
        
        Args:
            media_id: ID da mídia
        
        Returns:
            Dict com informações da mídia
        """
        self.logger.info(f"Obtendo status da mídia: {media_id}")
        
        try:
            url = f"{self.base_url}/{media_id}"
            params = {
                'access_token': self.access_token,
                'fields': 'id,media_type,media_url,permalink,timestamp,caption,like_count,comments_count'
            }
            
            response = self._make_request('GET', url, params=params)
            
            return {
                'success': True,
                'data': response,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao obter status: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Obtém informações da conta Instagram
        
        Returns:
            Dict com informações da conta
        """
        self.logger.info("Obtendo informações da conta")
        
        try:
            url = f"{self.base_url}/{self.account_id}"
            params = {
                'access_token': self.access_token,
                'fields': 'id,username,followers_count,follows_count,media_count,biography,website'
            }
            
            response = self._make_request('GET', url, params=params)
            
            return {
                'success': True,
                'data': response,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao obter informações da conta: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _make_request(self, method: str, url: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None, files: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Faz uma requisição HTTP com retry
        
        Args:
            method: Método HTTP (GET, POST, etc)
            url: URL da requisição
            data: Dados para enviar
            params: Parâmetros da URL
            files: Arquivos para upload
        
        Returns:
            Dict com a resposta
        """
        retries = 0
        last_error = None
        
        while retries < self.max_retries:
            try:
                self.logger.debug(f"Requisição {method} para {url}")
                
                if method.upper() == 'GET':
                    response = requests.get(
                        url, 
                        params=params, 
                        timeout=self.timeout
                    )
                elif method.upper() == 'POST':
                    if files:
                        response = requests.post(
                            url, 
                            data=data, 
                            files=files, 
                            timeout=self.timeout
                        )
                    else:
                        response = requests.post(
                            url, 
                            json=data, 
                            params=params, 
                            timeout=self.timeout
                        )
                else:
                    raise ValueError(f"Método HTTP não suportado: {method}")
                
                # Verifica se a resposta foi bem sucedida
                if response.status_code == 200:
                    return response.json()
                else:
                    error_msg = f"Erro {response.status_code}: {response.text}"
                    self.logger.warning(error_msg)
                    
                    # Se for erro de rate limit, espera mais tempo
                    if response.status_code == 429:
                        retry_after = int(response.headers.get('Retry-After', self.retry_delay))
                        self.logger.warning(f"Rate limit. Aguardando {retry_after} segundos...")
                        time.sleep(retry_after)
                        retries += 1
                        continue
                    
                    raise Exception(error_msg)
                    
            except requests.exceptions.Timeout:
                last_error = "Timeout na requisição"
                self.logger.warning(f"{last_error}. Tentativa {retries + 1}/{self.max_retries}")
                retries += 1
                time.sleep(self.retry_delay)
                
            except requests.exceptions.ConnectionError:
                last_error = "Erro de conexão"
                self.logger.warning(f"{last_error}. Tentativa {retries + 1}/{self.max_retries}")
                retries += 1
                time.sleep(self.retry_delay)
                
            except Exception as e:
                last_error = str(e)
                self.logger.warning(f"Erro: {last_error}. Tentativa {retries + 1}/{self.max_retries}")
                retries += 1
                time.sleep(self.retry_delay)
        
        raise Exception(f"Falha após {self.max_retries} tentativas: {last_error}")
    
    def close(self):
        """
        Fecha o cliente e libera recursos
        """
        self.logger.info("Fechando Instagram Client")
        # Não há recursos específicos para fechar

# Para testes
if __name__ == "__main__":
    # Teste básico
    client = InstagramClient()
    print("Client instanciado com sucesso!")
    print(f"Account ID: {client.account_id}")
    print(f"API Version: {client.api_version}")