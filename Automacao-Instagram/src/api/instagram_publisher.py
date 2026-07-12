#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Instagram Publisher - Módulo principal de publicação
Version: 1.0.0
"""

import os
import time
import json
import random
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

from src.utils.logger import get_logger
from src.api.instagram_client import InstagramClient
from src.models.post import Post, Story, Carousel

class InstagramPublisher:
    """
    Publicador de conteúdo para Instagram
    """
    
    def __init__(self, config_path: str = "./config/config.json"):
        """
        Inicializa o publicador
        
        Args:
            config_path: Caminho do arquivo de configuração
        """
        self.logger = get_logger(__name__)
        self.client = InstagramClient(config_path)
        self.publication_history = []
        self.failed_posts = []
        
        # Carrega configurações
        self.config_path = config_path
        
        self.logger.info("Instagram Publisher inicializado")
    
    def publish_post(self, post: Post) -> Dict[str, Any]:
        """
        Publica um post
        
        Args:
            post: Objeto Post
        
        Returns:
            Dict com resultado da publicação
        """
        self.logger.info(f"Publicando post: {post.image_path}")
        
        try:
            # Verifica se o post já foi publicado
            if self.is_post_published(post.image_path):
                self.logger.warning(f"Post já foi publicado: {post.image_path}")
                return {
                    'success': False,
                    'error': 'Post já publicado anteriormente',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Formata a legenda
            caption = self._format_caption(post.caption, post.hashtags)
            
            # Publica
            result = self.client.publish_post(
                image_path=post.image_path,
                caption=caption,
                location_id=post.location_id
            )
            
            # Registra histórico
            if result['success']:
                history_entry = {
                    'type': 'post',
                    'image_path': post.image_path,
                    'media_id': result.get('media_id'),
                    'timestamp': result.get('timestamp'),
                    'caption': caption,
                    'success': True
                }
                self.publication_history.append(history_entry)
                self._save_history()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao publicar post: {str(e)}")
            self.failed_posts.append({
                'post': post,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def publish_story(self, story: Story) -> Dict[str, Any]:
        """
        Publica um story
        
        Args:
            story: Objeto Story
        
        Returns:
            Dict com resultado da publicação
        """
        self.logger.info(f"Publicando story: {story.image_path}")
        
        try:
            # Verifica se o story já foi publicado
            if self.is_story_published(story.image_path):
                self.logger.warning(f"Story já foi publicado: {story.image_path}")
                return {
                    'success': False,
                    'error': 'Story já publicado anteriormente',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Publica
            result = self.client.publish_story(
                image_path=story.image_path,
                duration=story.duration
            )
            
            # Registra histórico
            if result['success']:
                history_entry = {
                    'type': 'story',
                    'image_path': story.image_path,
                    'story_id': result.get('story_id'),
                    'timestamp': result.get('timestamp'),
                    'duration': story.duration,
                    'success': True
                }
                self.publication_history.append(history_entry)
                self._save_history()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao publicar story: {str(e)}")
            self.failed_posts.append({
                'story': story,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def publish_carousel(self, carousel: Carousel) -> Dict[str, Any]:
        """
        Publica um carrossel
        
        Args:
            carousel: Objeto Carousel
        
        Returns:
            Dict com resultado da publicação
        """
        self.logger.info(f"Publicando carrossel com {len(carousel.image_paths)} imagens")
        
        try:
            # Verifica se as imagens já foram publicadas
            published_count = 0
            for img_path in carousel.image_paths:
                if self.is_post_published(img_path):
                    published_count += 1
            
            if published_count == len(carousel.image_paths):
                self.logger.warning("Todas as imagens do carrossel já foram publicadas")
                return {
                    'success': False,
                    'error': 'Todas as imagens já foram publicadas',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Formata a legenda
            caption = self._format_caption(carousel.caption, carousel.hashtags)
            
            # Publica
            result = self.client.publish_carousel(
                image_paths=carousel.image_paths,
                caption=caption
            )
            
            # Registra histórico
            if result['success']:
                for img_path in carousel.image_paths:
                    history_entry = {
                        'type': 'carousel',
                        'image_path': img_path,
                        'carousel_id': result.get('carousel_id'),
                        'timestamp': result.get('timestamp'),
                        'success': True
                    }
                    self.publication_history.append(history_entry)
                self._save_history()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao publicar carrossel: {str(e)}")
            self.failed_posts.append({
                'carousel': carousel,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_posts_from_directory(self, directory: str) -> List[Post]:
        """
        Obtém todos os posts de um diretório
        
        Args:
            directory: Caminho do diretório
        
        Returns:
            Lista de objetos Post
        """
        self.logger.info(f"Carregando posts do diretório: {directory}")
        
        posts = []
        path = Path(directory)
        
        if not path.exists():
            self.logger.warning(f"Diretório não encontrado: {directory}")
            return posts
        
        # Extensões suportadas
        supported_formats = ['.jpg', '.jpeg', '.png', '.mp4']
        
        for file_path in path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                # Tenta carregar um arquivo de legenda associado
                caption_file = file_path.with_suffix('.txt')
                caption = ""
                hashtags = []
                
                if caption_file.exists():
                    with open(caption_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.startswith('#hashtags:'):
                                hashtags = line.replace('#hashtags:', '').strip().split(',')
                            elif line.startswith('#caption:'):
                                caption = line.replace('#caption:', '').strip()
                            else:
                                caption += line
                
                # Se não houver arquivo de legenda, usa o nome do arquivo
                if not caption:
                    caption = file_path.stem.replace('_', ' ').replace('-', ' ')
                
                post = Post(
                    image_path=str(file_path),
                    caption=caption,
                    hashtags=hashtags if hashtags else self._generate_hashtags(),
                    scheduled_time=datetime.now()
                )
                posts.append(post)
        
        self.logger.info(f"Encontrados {len(posts)} posts em {directory}")
        return posts
    
    def get_stories_from_directory(self, directory: str) -> List[Story]:
        """
        Obtém todos os stories de um diretório
        
        Args:
            directory: Caminho do diretório
        
        Returns:
            Lista de objetos Story
        """
        self.logger.info(f"Carregando stories do diretório: {directory}")
        
        stories = []
        path = Path(directory)
        
        if not path.exists():
            self.logger.warning(f"Diretório não encontrado: {directory}")
            return stories
        
        # Extensões suportadas
        supported_formats = ['.jpg', '.jpeg', '.png', '.mp4']
        
        for file_path in path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                story = Story(
                    image_path=str(file_path),
                    duration=15,
                    scheduled_time=datetime.now()
                )
                stories.append(story)
        
        self.logger.info(f"Encontrados {len(stories)} stories em {directory}")
        return stories
    
    def publish_daily_posts(self) -> Dict[str, Any]:
        """
        Publica os posts diários automaticamente
        
        Returns:
            Dict com resultado da operação
        """
        self.logger.info("Iniciando publicação diária de posts")
        
        # Caminhos das pastas
        posts_dir = os.getenv('POSTS_PATH', './assets/posts')
        
        # Carrega posts
        posts = self.get_posts_from_directory(posts_dir)
        
        if not posts:
            self.logger.warning("Nenhum post encontrado para publicar")
            return {
                'success': False,
                'error': 'Nenhum post encontrado',
                'timestamp': datetime.now().isoformat()
            }
        
        # Filtra posts já publicados
        available_posts = [p for p in posts if not self.is_post_published(p.image_path)]
        
        if not available_posts:
            self.logger.warning("Todos os posts já foram publicados")
            return {
                'success': False,
                'error': 'Todos os posts já foram publicados',
                'timestamp': datetime.now().isoformat()
            }
        
        # Seleciona um post aleatório
        selected_post = random.choice(available_posts)
        self.logger.info(f"Post selecionado: {selected_post.image_path}")
        
        # Publica
        result = self.publish_post(selected_post)
        
        return result
    
    def publish_daily_stories(self) -> Dict[str, Any]:
        """
        Publica os stories diários automaticamente
        
        Returns:
            Dict com resultado da operação
        """
        self.logger.info("Iniciando publicação diária de stories")
        
        # Caminhos das pastas
        stories_dir = os.getenv('STORIES_PATH', './assets/stories')
        
        # Carrega stories
        stories = self.get_stories_from_directory(stories_dir)
        
        if not stories:
            self.logger.warning("Nenhum story encontrado para publicar")
            return {
                'success': False,
                'error': 'Nenhum story encontrado',
                'timestamp': datetime.now().isoformat()
            }
        
        # Filtra stories já publicados
        available_stories = [s for s in stories if not self.is_story_published(s.image_path)]
        
        if not available_stories:
            self.logger.warning("Todos os stories já foram publicados")
            return {
                'success': False,
                'error': 'Todos os stories já foram publicados',
                'timestamp': datetime.now().isoformat()
            }
        
        # Seleciona um story aleatório
        selected_story = random.choice(available_stories)
        self.logger.info(f"Story selecionado: {selected_story.image_path}")
        
        # Publica
        result = self.publish_story(selected_story)
        
        return result
    
    def is_post_published(self, image_path: str) -> bool:
        """
        Verifica se um post já foi publicado
        
        Args:
            image_path: Caminho da imagem
        
        Returns:
            True se já publicado, False caso contrário
        """
        for entry in self.publication_history:
            if entry.get('image_path') == image_path and entry.get('success', False):
                return True
        return False
    
    def is_story_published(self, image_path: str) -> bool:
        """
        Verifica se um story já foi publicado
        
        Args:
            image_path: Caminho da imagem
        
        Returns:
            True se já publicado, False caso contrário
        """
        for entry in self.publication_history:
            if entry.get('image_path') == image_path and entry.get('success', False):
                return True
        return False
    
    def _format_caption(self, caption: str, hashtags: List[str]) -> str:
        """
        Formata a legenda com hashtags
        
        Args:
            caption: Texto da legenda
            hashtags: Lista de hashtags
        
        Returns:
            Legenda formatada
        """
        if hashtags:
            hashtag_text = ' '.join([f'#{tag.replace(" ", "")}' for tag in hashtags])
            return f"{caption}\n\n{hashtag_text}"
        return caption
    
    def _generate_hashtags(self) -> List[str]:
        """
        Gera hashtags padrão
        
        Returns:
            Lista de hashtags
        """
        default_hashtags = [
            'Instagram',
            'Automacao',
            'Posts',
            'SocialMedia',
            'MarketingDigital',
            'ConteudoDigital',
            'Criatividade'
        ]
        return default_hashtags
    
    def _save_history(self):
        """
        Salva o histórico de publicações em arquivo
        """
        try:
            history_file = './logs/publication_history.json'
            os.makedirs(os.path.dirname(history_file), exist_ok=True)
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.publication_history, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"Histórico salvo: {len(self.publication_history)} entradas")
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar histórico: {str(e)}")
    
    def load_history(self):
        """
        Carrega o histórico de publicações
        """
        try:
            history_file = './logs/publication_history.json'
            
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.publication_history = json.load(f)
                self.logger.info(f"Histórico carregado: {len(self.publication_history)} entradas")
            else:
                self.logger.info("Nenhum histórico encontrado. Iniciando do zero.")
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar histórico: {str(e)}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas de publicações
        
        Returns:
            Dict com estatísticas
        """
        total_posts = len([e for e in self.publication_history if e.get('type') == 'post' and e.get('success')])
        total_stories = len([e for e in self.publication_history if e.get('type') == 'story' and e.get('success')])
        total_failures = len(self.failed_posts)
        
        return {
            'total_posts': total_posts,
            'total_stories': total_stories,
            'total_publications': total_posts + total_stories,
            'total_failures': total_failures,
            'success_rate': (total_posts + total_stories) / (total_posts + total_stories + total_failures) * 100 if (total_posts + total_stories + total_failures) > 0 else 0,
            'last_publication': self.publication_history[-1] if self.publication_history else None,
            'timestamp': datetime.now().isoformat()
        }
    
    def close(self):
        """
        Fecha o publicador e libera recursos
        """
        self.logger.info("Fechando Instagram Publisher")
        self.client.close()

# Para testes
if __name__ == "__main__":
    publisher = InstagramPublisher()
    print("Publisher instanciado com sucesso!")
    
    # Testa carregamento de posts
    posts = publisher.get_posts_from_directory("./assets/posts")
    print(f"Posts encontrados: {len(posts)}")
    
    # Testa carregamento de stories
    stories = publisher.get_stories_from_directory("./assets/stories")
    print(f"Stories encontrados: {len(stories)}")
    
    # Mostra estatísticas
    stats = publisher.get_statistics()
    print(f"Estatísticas: {json.dumps(stats, indent=2)}")