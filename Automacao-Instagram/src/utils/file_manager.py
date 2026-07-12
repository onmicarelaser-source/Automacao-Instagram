#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File Manager - Gerenciamento de arquivos e diretórios
Version: 1.0.0
"""

import os
import shutil
import hashlib
import json
import csv
from typing import List, Dict, Any, Optional, BinaryIO
from pathlib import Path
from datetime import datetime, timedelta
from PIL import Image

from src.utils.logger import get_logger

class FileManager:
    """
    Gerenciador de arquivos
    """
    
    def __init__(self):
        """
        Inicializa o gerenciador
        """
        self.logger = get_logger(__name__)
    
    def create_directory(self, path: str, exist_ok: bool = True) -> bool:
        """
        Cria um diretório
        
        Args:
            path: Caminho do diretório
            exist_ok: Se pode existir previamente
        
        Returns:
            True se criado com sucesso
        """
        try:
            os.makedirs(path, exist_ok=exist_ok)
            self.logger.debug(f"Diretório criado: {path}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao criar diretório {path}: {str(e)}")
            return False
    
    def file_exists(self, path: str) -> bool:
        """
        Verifica se um arquivo existe
        
        Args:
            path: Caminho do arquivo
        
        Returns:
            True se existe
        """
        return os.path.exists(path) and os.path.isfile(path)
    
    def directory_exists(self, path: str) -> bool:
        """
        Verifica se um diretório existe
        
        Args:
            path: Caminho do diretório
        
        Returns:
            True se existe
        """
        return os.path.exists(path) and os.path.isdir(path)
    
    def copy_file(self, source: str, destination: str) -> bool:
        """
        Copia um arquivo
        
        Args:
            source: Arquivo origem
            destination: Arquivo destino
        
        Returns:
            True se copiado com sucesso
        """
        try:
            shutil.copy2(source, destination)
            self.logger.debug(f"Arquivo copiado: {source} -> {destination}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao copiar arquivo: {str(e)}")
            return False
    
    def move_file(self, source: str, destination: str) -> bool:
        """
        Move um arquivo
        
        Args:
            source: Arquivo origem
            destination: Arquivo destino
        
        Returns:
            True se movido com sucesso
        """
        try:
            shutil.move(source, destination)
            self.logger.debug(f"Arquivo movido: {source} -> {destination}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao mover arquivo: {str(e)}")
            return False
    
    def delete_file(self, path: str) -> bool:
        """
        Deleta um arquivo
        
        Args:
            path: Caminho do arquivo
        
        Returns:
            True se deletado com sucesso
        """
        try:
            if self.file_exists(path):
                os.remove(path)
                self.logger.debug(f"Arquivo deletado: {path}")
                return True
            else:
                self.logger.warning(f"Arquivo não encontrado: {path}")
                return False
        except Exception as e:
            self.logger.error(f"Erro ao deletar arquivo: {str(e)}")
            return False
    
    def get_file_info(self, path: str) -> Dict[str, Any]:
        """
        Obtém informações de um arquivo
        
        Args:
            path: Caminho do arquivo
        
        Returns:
            Dict com informações do arquivo
        """
        if not self.file_exists(path):
            return {}
        
        try:
            stat = os.stat(path)
            info = {
                'path': path,
                'name': os.path.basename(path),
                'size': stat.st_size,
                'size_mb': stat.st_size / (1024 * 1024),
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'accessed': datetime.fromtimestamp(stat.st_atime),
                'is_file': os.path.isfile(path),
                'is_directory': os.path.isdir(path)
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Erro ao obter informações do arquivo: {str(e)}")
            return {}
    
    def get_directory_content(self, path: str, recursive: bool = False) -> List[Dict[str, Any]]:
        """
        Obtém o conteúdo de um diretório
        
        Args:
            path: Caminho do diretório
            recursive: Se deve listar recursivamente
        
        Returns:
            Lista de informações dos arquivos
        """
        if not self.directory_exists(path):
            return []
        
        try:
            content = []
            if recursive:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        info = self.get_file_info(file_path)
                        if info:
                            content.append(info)
                    for dir_name in dirs:
                        dir_path = os.path.join(root, dir_name)
                        info = self.get_file_info(dir_path)
                        if info:
                            content.append(info)
            else:
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    info = self.get_file_info(item_path)
                    if info:
                        content.append(info)
            
            return content
            
        except Exception as e:
            self.logger.error(f"Erro ao listar diretório: {str(e)}")
            return []
    
    def get_file_extension(self, path: str) -> str:
        """
        Obtém a extensão de um arquivo
        
        Args:
            path: Caminho do arquivo
        
        Returns:
            Extensão do arquivo
        """
        return os.path.splitext(path)[1].lower()
    
    def get_file_name(self, path: str) -> str:
        """
        Obtém o nome do arquivo sem extensão
        
        Args:
            path: Caminho do arquivo
        
        Returns:
            Nome do arquivo
        """
        return os.path.splitext(os.path.basename(path))[0]
    
    def get_file_hash(self, path: str, algorithm: str = 'sha256') -> Optional[str]:
        """
        Calcula o hash de um arquivo
        
        Args:
            path: Caminho do arquivo
            algorithm: Algoritmo de hash (md5, sha1, sha256)
        
        Returns:
            Hash do arquivo
        """
        if not self.file_exists(path):
            return None
        
        try:
            hash_func = hashlib.new(algorithm)
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular hash: {str(e)}")
            return None
    
    def backup_file(self, path: str, backup_dir: str) -> bool:
        """
        Cria um backup de um arquivo
        
        Args:
            path: Caminho do arquivo
            backup_dir: Diretório de backup
        
        Returns:
            True se backup criado com sucesso
        """
        if not self.file_exists(path):
            return False
        
        try:
            # Cria diretório de backup
            self.create_directory(backup_dir)
            
            # Gera nome do backup
            file_name = self.get_file_name(path)
            extension = self.get_file_extension(path)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{file_name}_backup_{timestamp}{extension}"
            backup_path = os.path.join(backup_dir, backup_name)
            
            # Copia o arquivo
            return self.copy_file(path, backup_path)
            
        except Exception as e:
            self.logger.error(f"Erro ao criar backup: {str(e)}")
            return False
    
    def compress_file(self, path: str, output_path: Optional[str] = None) -> Optional[str]:
        """
        Comprime um arquivo (usando ZIP)
        
        Args:
            path: Caminho do arquivo
            output_path: Caminho de saída (opcional)
        
        Returns:
            Caminho do arquivo comprimido
        """
        try:
            import zipfile
            
            if not self.file_exists(path):
                return None
            
            if not output_path:
                base_name = self.get_file_name(path)
                output_path = f"{base_name}.zip"
            
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(path, os.path.basename(path))
            
            self.logger.debug(f"Arquivo comprimido: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Erro ao comprimir arquivo: {str(e)}")
            return None
    
    def decompress_file(self, path: str, output_dir: Optional[str] = None) -> bool:
        """
        Descomprime um arquivo
        
        Args:
            path: Caminho do arquivo ZIP
            output_dir: Diretório de saída (opcional)
        
        Returns:
            True se descomprimido com sucesso
        """
        try:
            import zipfile
            
            if not self.file_exists(path):
                return False
            
            if not output_dir:
                output_dir = os.path.dirname(path)
            
            self.create_directory(output_dir)
            
            with zipfile.ZipFile(path, 'r') as zipf:
                zipf.extractall(output_dir)
            
            self.logger.debug(f"Arquivo descomprimido: {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao descomprimir arquivo: {str(e)}")
            return False
    
    def read_json(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Lê um arquivo JSON
        
        Args:
            path: Caminho do arquivo
        
        Returns:
            Dict com os dados
        """
        if not self.file_exists(path):
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Erro ao ler JSON: {str(e)}")
            return None
    
    def write_json(self, path: str, data: Dict[str, Any]) -> bool:
        """
        Escreve um arquivo JSON
        
        Args:
            path: Caminho do arquivo
            data: Dados a serem escritos
        
        Returns:
            True se escrito com sucesso
        """
        try:
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"JSON escrito: {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao escrever JSON: {str(e)}")
            return False
    
    def read_csv(self, path: str) -> List[Dict[str, Any]]:
        """
        Lê um arquivo CSV
        
        Args:
            path: Caminho do arquivo
        
        Returns:
            Lista de dicionários com os dados
        """
        if not self.file_exists(path):
            return []
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            self.logger.error(f"Erro ao ler CSV: {str(e)}")
            return []
    
    def write_csv(self, path: str, data: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None) -> bool:
        """
        Escreve um arquivo CSV
        
        Args:
            path: Caminho do arquivo
            data: Dados a serem escritos
            fieldnames: Nomes das colunas (opcional)
        
        Returns:
            True se escrito com sucesso
        """
        try:
            if not data:
                return False
            
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            if not fieldnames:
                fieldnames = data[0].keys()
            
            with open(path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            self.logger.debug(f"CSV escrito: {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao escrever CSV: {str(e)}")
            return False
    
    def read_text(self, path: str) -> Optional[str]:
        """
        Lê um arquivo de texto
        
        Args:
            path: Caminho do arquivo
        
        Returns:
            Conteúdo do arquivo
        """
        if not self.file_exists(path):
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Erro ao ler texto: {str(e)}")
            return None
    
    def write_text(self, path: str, content: str) -> bool:
        """
        Escreve um arquivo de texto
        
        Args:
            path: Caminho do arquivo
            content: Conteúdo a ser escrito
        
        Returns:
            True se escrito com sucesso
        """
        try:
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.debug(f"Texto escrito: {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao escrever texto: {str(e)}")
            return False
    
    def get_image_info(self, path: str) -> Dict[str, Any]:
        """
        Obtém informações de uma imagem
        
        Args:
            path: Caminho da imagem
        
        Returns:
            Dict com informações
        """
        if not self.file_exists(path):
            return {}
        
        try:
            with Image.open(path) as img:
                info = {
                    'path': path,
                    'format': img.format,
                    'mode': img.mode,
                    'width': img.width,
                    'height': img.height,
                    'size': img.size,
                    'pixels': img.width * img.height,
                    'aspect_ratio': img.width / img.height if img.height > 0 else 0
                }
                
                # Tenta obter EXIF
                try:
                    exif = img._getexif()
                    if exif:
                        info['exif'] = exif
                except:
                    pass
                
                return info
                
        except Exception as e:
            self.logger.error(f"Erro ao obter informações da imagem: {str(e)}")
            return {}
    
    def resize_image(self, path: str, width: int, height: int, output_path: Optional[str] = None) -> bool:
        """
        Redimensiona uma imagem
        
        Args:
            path: Caminho da imagem
            width: Largura desejada
            height: Altura desejada
            output_path: Caminho de saída (opcional)
        
        Returns:
            True se redimensionado com sucesso
        """
        if not self.file_exists(path):
            return False
        
        try:
            if not output_path:
                base_name = self.get_file_name(path)
                extension = self.get_file_extension(path)
                output_path = f"{base_name}_resized{extension}"
            
            with Image.open(path) as img:
                resized = img.resize((width, height), Image.Resampling.LANCZOS)
                resized.save(output_path)
            
            self.logger.debug(f"Imagem redimensionada: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao redimensionar imagem: {str(e)}")
            return False
    
    def cleanup_old_files(self, directory: str, days: int, pattern: Optional[str] = None) -> int:
        """
        Limpa arquivos antigos de um diretório
        
        Args:
            directory: Diretório a ser limpo
            days: Dias de retenção
            pattern: Padrão de nome (opcional)
        
        Returns:
            Número de arquivos deletados
        """
        if not self.directory_exists(directory):
            return 0
        
        try:
            cutoff = datetime.now() - timedelta(days=days)
            deleted = 0
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Verifica padrão
                    if pattern and not self._matches_pattern(file, pattern):
                        continue
                    
                    # Verifica data de modificação
                    mtime = os.path.getmtime(file_path)
                    file_date = datetime.fromtimestamp(mtime)
                    
                    if file_date < cutoff:
                        if self.delete_file(file_path):
                            deleted += 1
            
            self.logger.info(f"Limpeza concluída: {deleted} arquivos deletados de {directory}")
            return deleted
            
        except Exception as e:
            self.logger.error(f"Erro ao limpar arquivos: {str(e)}")
            return 0
    
    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """
        Verifica se um arquivo corresponde a um padrão
        
        Args:
            filename: Nome do arquivo
            pattern: Padrão (aceita * e ?)
        
        Returns:
            True se corresponde
        """
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)

# Para testes
if __name__ == "__main__":
    file_manager = FileManager()
    
    # Testa criação de diretório
    file_manager.create_directory("./test_dir")
    
    # Testa escrita de texto
    file_manager.write_text("./test_dir/test.txt", "Conteúdo de teste")
    
    # Testa leitura de texto
    content = file_manager.read_text("./test_dir/test.txt")
    print(f"Conteúdo: {content}")
    
    # Testa informações do arquivo
    info = file_manager.get_file_info("./test_dir/test.txt")
    print(f"Info: {json.dumps(info, indent=2, default=str)}")
    
    # Testa hash
    hash_value = file_manager.get_file_hash("./test_dir/test.txt")
    print(f"Hash: {hash_value}")
    
    # Testa limpeza
    file_manager.cleanup_old_files("./test_dir", 1)