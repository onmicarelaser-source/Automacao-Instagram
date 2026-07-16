import requests
import time
from config.api_config import APIConfig

class InstagramPublisher:
    def __init__(self):
        self.access_token = APIConfig.INSTAGRAM_ACCESS_TOKEN
        self.account_id = APIConfig.INSTAGRAM_ACCOUNT_ID
        self.base_url = APIConfig.INSTAGRAM_BASE_URL
    
    def publicar_post(self, imagem_url, legenda):
        """
        Publica post no Instagram via API
        """
        print(f"📤 Publicando post...")
        
        try:
            # 1. Criar container
            container_url = f"{self.base_url}/{self.account_id}/media"
            
            params = {
                "image_url": imagem_url,
                "caption": legenda,
                "access_token": self.access_token
            }
            
            response = requests.post(container_url, params=params)
            data = response.json()
            
            if "id" not in data:
                print(f"Erro ao criar container: {data}")
                return False
            
            container_id = data["id"]
            
            # 2. Publicar
            publish_url = f"{self.base_url}/{self.account_id}/media_publish"
            publish_params = {
                "creation_id": container_id,
                "access_token": self.access_token
            }
            
            response = requests.post(publish_url, params=publish_params)
            result = response.json()
            
            if "id" in result:
                print(f"✅ Post publicado! ID: {result['id']}")
                return True
            else:
                print(f"Erro ao publicar: {result}")
                return False
                
        except Exception as e:
            print(f"Erro ao publicar post: {e}")
            return False
    
    def publicar_story(self, imagem_url, legenda=""):
        """
        Publica story no Instagram via API
        """
        print(f"📱 Publicando story...")
        
        try:
            # Story tem formato específico
            container_url = f"{self.base_url}/{self.account_id}/media"
            
            params = {
                "image_url": imagem_url,
                "media_type": "STORIES",
                "caption": legenda[:100],
                "access_token": self.access_token
            }
            
            response = requests.post(container_url, params=params)
            data = response.json()
            
            if "id" not in data:
                print(f"Erro ao criar story: {data}")
                return False
            
            container_id = data["id"]
            
            # Publicar story (não precisa do step 2 para stories)
            # Stories são publicados automaticamente
            print(f"✅ Story publicado! ID: {container_id}")
            return True
            
        except Exception as e:
            print(f"Erro ao publicar story: {e}")
            return False
    
    def publicar_reel(self, video_url, legenda, thumbnail_url=None):
        """
        Publica reel no Instagram via API
        """
        print(f"🎬 Publicando reel...")
        
        try:
            # Reel usa media_type VIDEO
            container_url = f"{self.base_url}/{self.account_id}/media"
            
            params = {
                "media_type": "VIDEO",
                "video_url": video_url,
                "caption": legenda,
                "access_token": self.access_token
            }
            
            if thumbnail_url:
                params["thumbnail_url"] = thumbnail_url
            
            response = requests.post(container_url, params=params)
            data = response.json()
            
            if "id" not in data:
                print(f"Erro ao criar reel: {data}")
                return False
            
            container_id = data["id"]
            
            # Publicar
            publish_url = f"{self.base_url}/{self.account_id}/media_publish"
            publish_params = {
                "creation_id": container_id,
                "access_token": self.access_token
            }
            
            response = requests.post(publish_url, params=publish_params)
            result = response.json()
            
            if "id" in result:
                print(f"✅ Reel publicado! ID: {result['id']}")
                return True
            else:
                print(f"Erro ao publicar reel: {result}")
                return False
                
        except Exception as e:
            print(f"Erro ao publicar reel: {e}")
            return False
