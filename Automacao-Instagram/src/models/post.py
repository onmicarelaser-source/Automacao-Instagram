#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Post Models - Modelos de dados para posts e stories
Version: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

class MediaType(Enum):
    """
    Tipos de mídia
    """
    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    STORY = "story"
    REEL = "reel"

class PostStatus(Enum):
    """
    Status do post
    """
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    DELETED = "deleted"

@dataclass
class Post:
    """
    Modelo para posts do Instagram
    """
    image_path: str
    caption: str = ""
    hashtags: List[str] = field(default_factory=list)
    location_id: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    published_time: Optional[datetime] = None
    media_id: Optional[str] = None
    status: PostStatus = PostStatus.DRAFT
    media_type: MediaType = MediaType.IMAGE
    is_carousel: bool = False
    carousel_items: List[str] = field(default_factory=list)
    likes_count: int = 0
    comments_count: int = 0
    engagement_rate: float = 0.0
    tags: List[str] = field(default_factory=list)
    mentions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """
        Pós-inicialização
        """
        if self.scheduled_time is None:
            self.scheduled_time = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte para dicionário
        
        Returns:
            Dict com os dados
        """
        return {
            'image_path': self.image_path,
            'caption': self.caption,
            'hashtags': self.hashtags,
            'location_id': self.location_id,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'published_time': self.published_time.isoformat() if self.published_time else None,
            'media_id': self.media_id,
            'status': self.status.value,
            'media_type': self.media_type.value,
            'is_carousel': self.is_carousel,
            'carousel_items': self.carousel_items,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'engagement_rate': self.engagement_rate,
            'tags': self.tags,
            'mentions': self.mentions,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Post':
        """
        Cria um Post a partir de um dicionário
        
        Args:
            data: Dicionário com os dados
        
        Returns:
            Post
        """
        return cls(
            image_path=data.get('image_path', ''),
            caption=data.get('caption', ''),
            hashtags=data.get('hashtags', []),
            location_id=data.get('location_id'),
            scheduled_time=datetime.fromisoformat(data['scheduled_time']) if data.get('scheduled_time') else None,
            published_time=datetime.fromisoformat(data['published_time']) if data.get('published_time') else None,
            media_id=data.get('media_id'),
            status=PostStatus(data.get('status', 'draft')),
            media_type=MediaType(data.get('media_type', 'image')),
            is_carousel=data.get('is_carousel', False),
            carousel_items=data.get('carousel_items', []),
            likes_count=data.get('likes_count', 0),
            comments_count=data.get('comments_count', 0),
            engagement_rate=data.get('engagement_rate', 0.0),
            tags=data.get('tags', []),
            mentions=data.get('mentions', []),
            metadata=data.get('metadata', {}),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else datetime.now()
        )

@dataclass
class Story:
    """
    Modelo para stories do Instagram
    """
    image_path: str
    duration: int = 15
    link: Optional[str] = None
    hashtags: List[str] = field(default_factory=list)
    mentions: List[str] = field(default_factory=list)
    location_id: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    published_time: Optional[datetime] = None
    story_id: Optional[str] = None
    status: PostStatus = PostStatus.DRAFT
    views_count: int = 0
    replies_count: int = 0
    is_archived: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """
        Pós-inicialização
        """
        if self.scheduled_time is None:
            self.scheduled_time = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte para dicionário
        
        Returns:
            Dict com os dados
        """
        return {
            'image_path': self.image_path,
            'duration': self.duration,
            'link': self.link,
            'hashtags': self.hashtags,
            'mentions': self.mentions,
            'location_id': self.location_id,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'published_time': self.published_time.isoformat() if self.published_time else None,
            'story_id': self.story_id,
            'status': self.status.value,
            'views_count': self.views_count,
            'replies_count': self.replies_count,
            'is_archived': self.is_archived,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Story':
        """
        Cria um Story a partir de um dicionário
        
        Args:
            data: Dicionário com os dados
        
        Returns:
            Story
        """
        return cls(
            image_path=data.get('image_path', ''),
            duration=data.get('duration', 15),
            link=data.get('link'),
            hashtags=data.get('hashtags', []),
            mentions=data.get('mentions', []),
            location_id=data.get('location_id'),
            scheduled_time=datetime.fromisoformat(data['scheduled_time']) if data.get('scheduled_time') else None,
            published_time=datetime.fromisoformat(data['published_time']) if data.get('published_time') else None,
            story_id=data.get('story_id'),
            status=PostStatus(data.get('status', 'draft')),
            views_count=data.get('views_count', 0),
            replies_count=data.get('replies_count', 0),
            is_archived=data.get('is_archived', False),
            metadata=data.get('metadata', {}),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else datetime.now()
        )

@dataclass
class Carousel:
    """
    Modelo para carrossel de posts
    """
    image_paths: List[str]
    caption: str = ""
    hashtags: List[str] = field(default_factory=list)
    location_id: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    published_time: Optional[datetime] = None
    carousel_id: Optional[str] = None
    status: PostStatus = PostStatus.DRAFT
    likes_count: int = 0
    comments_count: int = 0
    engagement_rate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """
        Pós-inicialização
        """
        if self.scheduled_time is None:
            self.scheduled_time = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte para dicionário
        
        Returns:
            Dict com os dados
        """
        return {
            'image_paths': self.image_paths,
            'caption': self.caption,
            'hashtags': self.hashtags,
            'location_id': self.location_id,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'published_time': self.published_time.isoformat() if self.published_time else None,
            'carousel_id': self.carousel_id,
            'status': self.status.value,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'engagement_rate': self.engagement_rate,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Carousel':
        """
        Cria um Carousel a partir de um dicionário
        
        Args:
            data: Dicionário com os dados
        
        Returns:
            Carousel
        """
        return cls(
            image_paths=data.get('image_paths', []),
            caption=data.get('caption', ''),
            hashtags=data.get('hashtags', []),
            location_id=data.get('location_id'),
            scheduled_time=datetime.fromisoformat(data['scheduled_time']) if data.get('scheduled_time') else None,
            published_time=datetime.fromisoformat(data['published_time']) if data.get('published_time') else None,
            carousel_id=data.get('carousel_id'),
            status=PostStatus(data.get('status', 'draft')),
            likes_count=data.get('likes_count', 0),
            comments_count=data.get('comments_count', 0),
            engagement_rate=data.get('engagement_rate', 0.0),
            metadata=data.get('metadata', {}),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else datetime.now()
        )

# Para testes
if __name__ == "__main__":
    # Testa Post
    post = Post(
        image_path="./test.jpg",
        caption="Teste de post",
        hashtags=["teste", "automacao"],
        scheduled_time=datetime(2024, 12, 31, 23, 59)
    )
    print("Post criado:")
    print(json.dumps(post.to_dict(), indent=2))
    
    # Testa Story
    story = Story(
        image_path="./story.jpg",
        duration=15,
        hashtags=["story", "teste"]
    )
    print("\nStory criado:")
    print(json.dumps(story.to_dict(), indent=2))