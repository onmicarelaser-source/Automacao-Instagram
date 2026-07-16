import requests
import json
from datetime import datetime
from config.api_config import APIConfig

class GeradorImagemCanva:
    def __init__(self):
        self.api_key = APIConfig.CANVA_API_KEY
        self.base_url = "https://api.canva.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def criar_post(self, tema, legenda):
        """Cria imagem para post via Canva API"""
        return self._criar_midia(tema, legenda, "post", APIConfig.CANVA_TEMPLATE_POST)
    
    def criar_story(self, tema, legenda):
        """Cria imagem para story via Canva API"""
        return self._criar_midia(tema, legenda, "story", APIConfig.CANVA_TEMPLATE_STORY)
    
    def criar_reel_thumbnail(self, tema):
        """Cria thumbnail para reel via Canva API"""
        return self._criar_midia(tema, "", "reel", APIConfig.CANVA_TEMPLATE_REEL)
    
    def _criar_midia(self, tema, legenda, tipo, template_id):
        if not template_id:
            return self._placeholder(tema, tipo)
        
        sizes = {
            "post": "1080x1080",
            "story": "1080x1920",
            "reel": "1080x1920"
        }
        
        payload = {
            "templateId": template_id,
            "replacements": {
                "tema": tema,
                "legenda": legenda[:100],
                "data": datetime.now().strftime("%d/%m/%Y")
            },
            "format": "jpg" if tipo != "reel" else "jpg",
            "size": sizes.get(tipo, "1080x1080")
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/designs",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("url"):
                    return data["url"]
            
            return self._placeholder(tema, tipo)
            
        except Exception as e:
            print(f"Erro Canva: {e}")
            return self._placeholder(tema, tipo)
    
    def _placeholder(self, tema, tipo):
        """Retorna URL de placeholder em caso de erro"""
        # Usar Pexels para buscar imagem relacionada
        if APIConfig.PEXELS_API_KEY:
            try:
                response = requests.get(
                    "https://api.pexels.com/v1/search",
                    headers={"Authorization": APIConfig.PEXELS_API_KEY},
                    params={"query": tema, "per_page": 1, "orientation": "square" if tipo != "story" else "portrait"}
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get("photos"):
                        return data["photos"][0]["src"]["large"]
            except:
                pass
        
        # Fallback final
        return f"https://via.placeholder.com/1080x1080/1A1A2E/FFFFFF?text={tema.replace(' ', '+')}"
