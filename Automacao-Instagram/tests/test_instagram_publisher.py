#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for Instagram Publisher
Version: 1.0.0
"""

import unittest
import os
import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api.instagram_publisher import InstagramPublisher
from src.models.post import Post, Story, Carousel
from src.utils.logger import setup_logger

class TestInstagramPublisher(unittest.TestCase):
    """
    Testes para o Instagram Publisher
    """
    
    def setUp(self):
        """
        Configuração dos testes
        """
        # Configura logger para testes
        self.logger = setup_logger(
            log_level="DEBUG",
            log_file="./logs/test.log",
            console_output=True
        )
        
        # Cria diretórios temporários para testes
        self.test_dir = tempfile.mkdtemp()
        self.posts_dir = os.path.join(self.test_dir, 'posts')
        self.stories_dir = os.path.join(self.test_dir, 'stories')
        os.makedirs(self.posts_dir, exist_ok=True)
        os.makedirs(self.stories_dir, exist_ok=True)
        
        # Cria arquivos de teste
        self.test_image = os.path.join(self.posts_dir, 'test.jpg')
        with open(self.test_image, 'w') as f:
            f.write('test image content')
        
        self.test_story = os.path.join(self.stories_dir, 'story.jpg')
        with open(self.test_story, 'w') as f:
            f.write('test story content')
        
        # Cria arquivo de legenda
        caption_file = os.path.join(self.posts_dir, 'test.txt')
        with open(caption_file, 'w') as f:
            f.write("#caption:Teste de post\n")
            f.write("#hashtags:teste,automacao,instagram\n")
        
        # Mock do InstagramClient
        self.publisher = InstagramPublisher()
        self.publisher.client = Mock()
    
    def test_publisher_initialization(self):
        """
        Testa a inicialização do publisher
        """
        self.assertIsNotNone(self.publisher)
        self.assertIsNotNone(self.publisher.client)
        self.assertIsInstance(self.publisher.publication_history, list)
    
    def test_get_posts_from_directory(self):
        """
        Testa o carregamento de posts do diretório
        """
        # Configura variável de ambiente
        os.environ['POSTS_PATH'] = self.posts_dir
        
        # Carrega posts
        posts = self.publisher.get_posts_from_directory(self.posts_dir)
        
        # Verifica
        self.assertGreater(len(posts), 0)
        self.assertIsInstance(posts[0], Post)
        self.assertEqual(posts[0].image_path, self.test_image)
        self.assertIn('teste', posts[0].hashtags)
    
    def test_get_stories_from_directory(self):
        """
        Testa o carregamento de stories do diretório
        """
        # Configura variável de ambiente
        os.environ['STORIES_PATH'] = self.stories_dir
        
        # Carrega stories
        stories = self.publisher.get_stories_from_directory(self.stories_dir)
        
        # Verifica
        self.assertGreater(len(stories), 0)
        self.assertIsInstance(stories[0], Story)
        self.assertEqual(stories[0].image_path, self.test_story)
    
    def test_publish_post_success(self):
        """
        Testa a publicação bem-sucedida de um post
        """
        # Mock da resposta do cliente
        self.publisher.client.publish_post.return_value = {
            'success': True,
            'media_id': '123456',
            'timestamp': datetime.now().isoformat()
        }
        
        # Cria um post
        post = Post(
            image_path=self.test_image,
            caption="Teste de post",
            hashtags=["teste"]
        )
        
        # Publica
        result = self.publisher.publish_post(post)
        
        # Verifica
        self.assertTrue(result['success'])
        self.assertEqual(result['media_id'], '123456')
        self.assertIn(post, self.publisher.publication_history)
    
    def test_publish_post_failure(self):
        """
        Testa a falha na publicação de um post
        """
        # Mock da resposta do cliente
        self.publisher.client.publish_post.return_value = {
            'success': False,
            'error': 'Erro de API',
            'timestamp': datetime.now().isoformat()
        }
        
        # Cria um post
        post = Post(
            image_path=self.test_image,
            caption="Teste de post"
        )
        
        # Publica
        result = self.publisher.publish_post(post)
        
        # Verifica
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Erro de API')
    
    def test_publish_story_success(self):
        """
        Testa a publicação bem-sucedida de um story
        """
        # Mock da resposta do cliente
        self.publisher.client.publish_story.return_value = {
            'success': True,
            'story_id': '789012',
            'timestamp': datetime.now().isoformat()
        }
        
        # Cria um story
        story = Story(
            image_path=self.test_story,
            duration=15
        )
        
        # Publica
        result = self.publisher.publish_story(story)
        
        # Verifica
        self.assertTrue(result['success'])
        self.assertEqual(result['story_id'], '789012')
    
    def test_is_post_published(self):
        """
        Testa a verificação de publicação de post
        """
        # Adiciona ao histórico
        self.publisher.publication_history.append({
            'type': 'post',
            'image_path': self.test_image,
            'success': True,
            'timestamp': datetime.now().isoformat()
        })
        
        # Verifica
        self.assertTrue(self.publisher.is_post_published(self.test_image))
        self.assertFalse(self.publisher.is_post_published('not_exists.jpg'))
    
    def test_is_story_published(self):
        """
        Testa a verificação de publicação de story
        """
        # Adiciona ao histórico
        self.publisher.publication_history.append({
            'type': 'story',
            'image_path': self.test_story,
            'success': True,
            'timestamp': datetime.now().isoformat()
        })
        
        # Verifica
        self.assertTrue(self.publisher.is_story_published(self.test_story))
        self.assertFalse(self.publisher.is_story_published('not_exists.jpg'))
    
    def test_format_caption(self):
        """
        Testa a formatação da legenda
        """
        caption = "Teste de legenda"
        hashtags = ["teste", "automacao", "instagram"]
        
        formatted = self.publisher._format_caption(caption, hashtags)
        
        self.assertIn(caption, formatted)
        self.assertIn("#teste", formatted)
        self.assertIn("#automacao", formatted)
        self.assertIn("#instagram", formatted)
    
    def test_generate_hashtags(self):
        """
        Testa a geração de hashtags
        """
        hashtags = self.publisher._generate_hashtags()
        
        self.assertIsInstance(hashtags, list)
        self.assertGreater(len(hashtags), 0)
        self.assertIn('Instagram', hashtags)
    
    def test_get_statistics(self):
        """
        Testa a obtenção de estatísticas
        """
        # Adiciona publicações
        self.publisher.publication_history = [
            {'type': 'post', 'success': True},
            {'type': 'story', 'success': True},
            {'type': 'post', 'success': False}
        ]
        self.publisher.failed_posts = [{'post': 'test'}]
        
        stats = self.publisher.get_statistics()
        
        self.assertEqual(stats['total_posts'], 1)  # Apenas os bem-sucedidos
        self.assertEqual(stats['total_stories'], 1)
        self.assertEqual(stats['total_publications'], 2)
        self.assertEqual(stats['total_failures'], 1)
        self.assertIsNotNone(stats['success_rate'])
    
    def test_save_and_load_history(self):
        """
        Testa o salvamento e carregamento do histórico
        """
        # Adiciona ao histórico
        test_entry = {
            'type': 'post',
            'image_path': self.test_image,
            'success': True,
            'timestamp': datetime.now().isoformat()
        }
        self.publisher.publication_history.append(test_entry)
        
        # Salva
        self.publisher._save_history()
        
        # Limpa
        self.publisher.publication_history = []
        
        # Carrega
        self.publisher.load_history()
        
        # Verifica
        self.assertEqual(len(self.publisher.publication_history), 1)
        self.assertEqual(self.publisher.publication_history[0]['image_path'], self.test_image)
    
    def test_publish_daily_posts(self):
        """
        Testa a publicação diária de posts
        """
        # Configura ambiente
        os.environ['POSTS_PATH'] = self.posts_dir
        
        # Mock da publicação
        self.publisher.client.publish_post.return_value = {
            'success': True,
            'media_id': '123456',
            'timestamp': datetime.now().isoformat()
        }
        
        # Publica
        result = self.publisher.publish_daily_posts()
        
        # Verifica
        self.assertTrue(result.get('success', False))
    
    def test_publish_daily_stories(self):
        """
        Testa a publicação diária de stories
        """
        # Configura ambiente
        os.environ['STORIES_PATH'] = self.stories_dir
        
        # Mock da publicação
        self.publisher.client.publish_story.return_value = {
            'success': True,
            'story_id': '789012',
            'timestamp': datetime.now().isoformat()
        }
        
        # Publica
        result = self.publisher.publish_daily_stories()
        
        # Verifica
        self.assertTrue(result.get('success', False))
    
    def tearDown(self):
        """
        Limpeza após os testes
        """
        # Remove arquivos temporários
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        
        # Limpa variáveis de ambiente
        os.environ.pop('POSTS_PATH', None)
        os.environ.pop('STORIES_PATH', None)

if __name__ == '__main__':
    unittest.main(verbosity=2)