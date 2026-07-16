import anthropic
import json
from config.api_config import APIConfig

class GeradorClaude:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=APIConfig.CLAUDE_API_KEY)
        self.model = APIConfig.CLAUDE_MODEL
    
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
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except:
            return "Ideias para posts geradas automaticamente."
