#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Content Model - Modelo de conteúdo
Version: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

class ContentType(Enum):
    """
    Tipos de conteúdo
    """
    POST = "post"
    STORY = "story"
    REEL = "reel"
    CAROUSEL = "carousel"
    IGTV = "igtv"
    LIVE = "live"

class ContentStatus(Enum):
    """
    Status do conteúdo
    """
    DRAFT = "draft"
    PENDING = "pending"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    DELETED = "deleted"
    ARCHIVED = "archived"

class ContentVisibility(Enum):
    """
    Visibilidade do conteúdo
    """
    PUBLIC = "public"
    PRIVATE = "private"
    FOLLOWERS = "followers"
    CLOSE_FRIENDS = "close_friends"

@dataclass
class Content:
    """
    Modelo base para conteúdo
    """
    id: str
    type: ContentType
    status: ContentStatus = ContentStatus.DRAFT
    visibility: ContentVisibility = ContentVisibility.PUBLIC
    title: str = ""
    description: str = ""
    hashtags: List[str] = field(default_factory=list)
    mentions: List[str] = field(default_factory=list)
    media_urls: List[str] = field(default_factory=list)
    thumbnail_url: Optional[str] = None
    location_id: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    published_time: Optional[datetime] = None
    platform_id: Optional[str] = None
    platform_url: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    views_count: int = 0
    engagement_rate: float = 0.0
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    
    def __post_init__(self):
        """
        Pós-inicialização
        """
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte para dicionário
        
        Returns:
            Dict com os dados
        """
        return {
            'id': self.id,
            'type': self.type.value,
            'status': self.status.value,
            'visibility': self.visibility.value,
            'title': self.title,
            'description': self.description,
            'hashtags': self.hashtags,
            'mentions': self.mentions,
            'media_urls': self.media_urls,
            'thumbnail_url': self.thumbnail_url,
            'location_id': self.location_id,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'published_time': self.published_time.isoformat() if self.published_time else None,
            'platform_id': self.platform_id,
            'platform_url': self.platform_url,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'shares_count': self.shares_count,
            'views_count': self.views_count,
            'engagement_rate': self.engagement_rate,
            'tags': self.tags,
            'categories': self.categories,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Content':
        """
        Cria um Content a partir de um dicionário
        
        Args:
            data: Dicionário com os dados
        
        Returns:
            Content
        """
        return cls(
            id=data.get('id', ''),
            type=ContentType(data.get('type', 'post')),
            status=ContentStatus(data.get('status', 'draft')),
            visibility=ContentVisibility(data.get('visibility', 'public')),
            title=data.get('title', ''),
            description=data.get('description', ''),
            hashtags=data.get('hashtags', []),
            mentions=data.get('mentions', []),
            media_urls=data.get('media_urls', []),
            thumbnail_url=data.get('thumbnail_url'),
            location_id=data.get('location_id'),
            scheduled_time=datetime.fromisoformat(data['scheduled_time']) if data.get('scheduled_time') else None,
            published_time=datetime.fromisoformat(data['published_time']) if data.get('published_time') else None,
            platform_id=data.get('platform_id'),
            platform_url=data.get('platform_url'),
            likes_count=data.get('likes_count', 0),
            comments_count=data.get('comments_count', 0),
            shares_count=data.get('shares_count', 0),
            views_count=data.get('views_count', 0),
            engagement_rate=data.get('engagement_rate', 0.0),
            tags=data.get('tags', []),
            categories=data.get('categories', []),
            metadata=data.get('metadata', {}),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else datetime.now(),
            created_by=data.get('created_by'),
            updated_by=data.get('updated_by')
        )
    
    def is_published(self) -> bool:
        """
        Verifica se o conteúdo está publicado
        
        Returns:
            True se publicado
        """
        return self.status == ContentStatus.PUBLISHED
    
    def is_scheduled(self) -> bool:
        """
        Verifica se o conteúdo está agendado
        
        Returns:
            True se agendado
        """
        return self.status == ContentStatus.SCHEDULED
    
    def is_draft(self) -> bool:
        """
        Verifica se o conteúdo é rascunho
        
        Returns:
            True se rascunho
        """
        return self.status == ContentStatus.DRAFT
    
    def get_engagement_rate(self) -> float:
        """
        Calcula a taxa de engajamento
        
        Returns:
            Taxa de engajamento
        """
        total_interactions = self.likes_count + self.comments_count + self.shares_count
        if self.views_count > 0:
            return (total_interactions / self.views_count) * 100
        return 0.0

@dataclass
class ContentBatch:
    """
    Lote de conteúdo para publicação
    """
    id: str
    name: str
    contents: List[Content] = field(default_factory=list)
    scheduled_time: Optional[datetime] = None
    published_time: Optional[datetime] = None
    status: ContentStatus = ContentStatus.DRAFT
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """
        Pós-inicialização
        """
        self.updated_at = datetime.now()
    
    def add_content(self, content: Content):
        """
        Adiciona conteúdo ao lote
        
        Args:
            content: Conteúdo a ser adicionado
        """
        self.contents.append(content)
        self.updated_at = datetime.now()
    
    def remove_content(self, content_id: str) -> bool:
        """
        Remove conteúdo do lote
        
        Args:
            content_id: ID do conteúdo
        
        Returns:
            True se removido
        """
        for i, content in enumerate(self.contents):
            if content.id == content_id:
                self.contents.pop(i)
                self.updated_at = datetime.now()
                return True
        return False
    
    def get_total_media_count(self) -> int:
        """
        Obtém o total de mídias no lote
        
        Returns:
            Número total de mídias
        """
        return sum(len(content.media_urls) for content in self.contents)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte para dicionário
        
        Returns:
            Dict com os dados
        """
        return {
            'id': self.id,
            'name': self.name,
            'contents': [content.to_dict() for content in self.contents],
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'published_time': self.published_time.isoformat() if self.published_time else None,
            'status': self.status.value,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Para testes
if __name__ == "__main__":
    import json
    from uuid import uuid4
    
    content = Content(
        id=str(uuid4()),
        type=ContentType.POST,
        title="Teste de conteúdo",
        description="Descrição do conteúdo",
        hashtags=["teste", "automacao"],
        media_urls=["https://exemplo.com/imagem.jpg"]
    )
    
    print("Content criado:")
    print(json.dumps(content.to_dict(), indent=2))
    
    # Testa batch
    batch = ContentBatch(
        id=str(uuid4()),
        name="Lote de Teste"
    )
    batch.add_content(content)
    print("\nBatch criado:")
    print(json.dumps(batch.to_dict(), indent=2))