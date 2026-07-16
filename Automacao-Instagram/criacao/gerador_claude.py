import importlib
import json
from config.api_config import APIConfig

class GeradorClaude:
    def __init__(self):
        self.available = False
        self.client = None
        self.model = APIConfig.CLAUDE_MODEL
        try:
            anthropic = importlib.import_module('anthropic')
            self.client = anthropic.Anthropic(api_key=APIConfig.CLAUDE_API_KEY)
            self.available = True
        except Exception as e:
            print(f"Aviso: Claude não disponível ({e})")
    
    def revisar_legenda(self, legenda, tema):
        """Revisa e melhora a legenda usando Claude"""
        
        prompt = f"""
        Revise e melhore esta legenda para Instagram.
        
        Tema: {tema}
        Legenda atual: {legenda}
        
        Melhore:
        - Tornar mais envolvente
        - Adicionar emojis estratégicos
        - Melhorar fluidez
        - Fortalecer o CTA
        
        Responda APENAS com a legenda revisada.
        """
        
        if not self.available:
            return legenda
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Erro Claude: {e}")
            return legenda
    
    def gerar_ideias(self, nicho="beleza", quantidade=5):
        """Gera ideias criativas usando Claude"""
        
        prompt = f"""
        Gere {quantidade} ideias criativas para posts no Instagram.
        
        Nicho: {nicho}
        
        Para cada ideia, inclua:
        - Título chamativo
        - Tipo (post/story/reel)
        - Descrição rápida
        - Sugestão de tom
        
        Formato: lista numerada.
        """
        
        if not self.available:
            return "Ideias para posts geradas automaticamente."
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Erro Claude: {e}")
            return "Ideias para posts geradas automaticamente."
