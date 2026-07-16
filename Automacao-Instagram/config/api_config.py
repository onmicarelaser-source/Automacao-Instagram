import os
from dotenv import load_dotenv

load_dotenv()

class APIConfig:
    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")
    
    # Claude
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
    
    # Canva
    CANVA_API_KEY = os.getenv("CANVA_API_KEY")
    CANVA_TEMPLATE_POST = os.getenv("CANVA_TEMPLATE_POST")
    CANVA_TEMPLATE_STORY = os.getenv("CANVA_TEMPLATE_STORY")
    CANVA_TEMPLATE_REEL = os.getenv("CANVA_TEMPLATE_REEL")
    
    # Instagram
    INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
    INSTAGRAM_BASE_URL = os.getenv("INSTAGRAM_BASE_URL", "https://graph.facebook.com/v17.0")
    
    # Pexels
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
    
    # Configurações
    VERIFICAR_INTERVALO = int(os.getenv("VERIFICAR_INTERVALO", 60))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validar(cls):
        erros = []
        if not cls.GEMINI_API_KEY:
            erros.append("GEMINI_API_KEY não configurada")
        if not cls.CLAUDE_API_KEY:
            erros.append("CLAUDE_API_KEY não configurada")
        if not cls.CANVA_API_KEY:
            erros.append("CANVA_API_KEY não configurada")
        if not cls.INSTAGRAM_ACCESS_TOKEN:
            erros.append("INSTAGRAM_ACCESS_TOKEN não configurado")
        if not cls.INSTAGRAM_ACCOUNT_ID:
            erros.append("INSTAGRAM_ACCOUNT_ID não configurado")
        
        if erros:
            raise Exception("Erros de configuração:\n" + "\n".join(erros))
        return True
