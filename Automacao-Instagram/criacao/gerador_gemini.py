import importlib
import json
from config.api_config import APIConfig

class GeradorGemini:
    def __init__(self):
        self.available = False
        self.model = None
        self.genai = None
        try:
            self.genai = importlib.import_module('google.generativeai')
            self.genai.configure(api_key=APIConfig.GEMINI_API_KEY)
            self.model = self.genai.GenerativeModel(APIConfig.GEMINI_MODEL)
            self.available = True
        except Exception as e:
            print(f"Aviso: Gemini não disponível ({e})")
    
    def gerar_legenda(self, tema, tipo="post", tom="profissional"):
        """Gera legenda usando Gemini"""
        
        prompt = f"""
        Crie uma legenda para um {tipo} no Instagram sobre: "{tema}"
        
        Tom: {tom}
        
        Responda APENAS com JSON:
        {{
            "legenda": "texto da legenda com emojis e quebras de linha",
            "hashtags": "#hashtag1 #hashtag2 #hashtag3",
            "cta": "chamada para ação"
        }}
        """
        
        if not self.available:
            return self._fallback(tema)
        try:
            response = self.model.generate_content(prompt)
            return self._parse_json(response.text, tema)
        except Exception as e:
            print(f"Erro Gemini: {e}")
            return self._fallback(tema)
    
    def gerar_script_reel(self, tema):
        """Gera script para reel usando Gemini"""
        
        prompt = f"""
        Crie um script para um Reel do Instagram sobre: "{tema}"
        
        Estrutura:
        1. Abertura (3 segundos)
        2. Desenvolvimento (10-15 segundos)
        3. Final com CTA (3 segundos)
        
        Inclua: texto, sugestões de cena, música sugerida.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return f"Script para Reel sobre {tema} - Crie um vídeo rápido e envolvente sobre este tema."
    
    def _parse_json(self, texto, tema):
        try:
            # Limpar texto
            inicio = texto.find('{')
            fim = texto.rfind('}') + 1
            if inicio >= 0 and fim > inicio:
                texto = texto[inicio:fim]
            return json.loads(texto)
        except:
            return {
                "legenda": f"🌟 {tema} 🌟\n\nDescubra essa novidade incrível!",
                "hashtags": f"#{tema.replace(' ', '').lower()} #onmicarelaser",
                "cta": "Comente e compartilhe!"
            }
    
    def _fallback(self, tema):
        return {
            "legenda": f"🌟 {tema} 🌟\n\nConfira essa novidade!\n\n👉 Link na bio!",
            "hashtags": f"#{tema.replace(' ', '').lower()} #onmicarelaser #instagram",
            "cta": "Curta e compartilhe!"
        }
