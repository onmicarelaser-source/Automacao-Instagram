#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
User Model - Modelo de usuário
Version: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class UserRole(Enum):
    """
    Papéis de usuário
    """
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    VIEWER = "viewer"

class AccountType(Enum):
    """
    Tipos de conta Instagram
    """
    PERSONAL = "personal"
    BUSINESS = "business"
    CREATOR = "creator"

@dataclass
class User:
    """
    Modelo de usuário do sistema
    """
    username: str
    email: str
    password_hash: str
    instagram_username: str = ""
    instagram_account_id: str = ""
    account_type: AccountType = AccountType.PERSONAL
    role: UserRole = UserRole.USER
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    settings: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
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
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'instagram_username': self.instagram_username,
            'instagram_account_id': self.instagram_account_id,
            'account_type': self.account_type.value,
            'role': self.role.value,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'token_expires_at': self.token_expires_at.isoformat() if self.token_expires_at else None,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'settings': self.settings,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Cria um User a partir de um dicionário
        
        Args:
            data: Dicionário com os dados
        
        Returns:
            User
        """
        return cls(
            username=data.get('username', ''),
            email=data.get('email', ''),
            password_hash=data.get('password_hash', ''),
            instagram_username=data.get('instagram_username', ''),
            instagram_account_id=data.get('instagram_account_id', ''),
            account_type=AccountType(data.get('account_type', 'personal')),
            role=UserRole(data.get('role', 'user')),
            access_token=data.get('access_token'),
            refresh_token=data.get('refresh_token'),
            token_expires_at=datetime.fromisoformat(data['token_expires_at']) if data.get('token_expires_at') else None,
            is_active=data.get('is_active', True),
            is_verified=data.get('is_verified', False),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else datetime.now(),
            last_login=datetime.fromisoformat(data['last_login']) if data.get('last_login') else None,
            settings=data.get('settings', {}),
            metadata=data.get('metadata', {})
        )
    
    def is_token_expired(self) -> bool:
        """
        Verifica se o token está expirado
        
        Returns:
            True se expirado
        """
        if not self.token_expires_at:
            return True
        return datetime.now() >= self.token_expires_at
    
    def can_publish(self) -> bool:
        """
        Verifica se o usuário pode publicar
        
        Returns:
            True se pode publicar
        """
        return self.is_active and self.is_verified and bool(self.access_token)

# Para testes
if __name__ == "__main__":
    user = User(
        username="test_user",
        email="test@example.com",
        password_hash="hashed_password"
    )
    print("User criado:")
    print(json.dumps(user.to_dict(), indent=2))