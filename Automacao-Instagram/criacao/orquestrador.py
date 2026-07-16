from .gerador_gemini import GeradorGemini
from .gerador_claude import GeradorClaude
from .gerador_imagem_canva import GeradorImagemCanva
import time

class OrquestradorConteudo:
    def __init__(self):
        self.gemini = GeradorGemini()
        self.claude = GeradorClaude()
        self.canva = GeradorImagemCanva()
    
    def criar_conteudo_completo(self, tema, tipo="post", tom="profissional"):
        """
        Cria conteúdo completo (texto + imagem) usando todas as APIs
        
        Returns:
            dict: {
                "legenda": "texto",
                "hashtags": "#hashtags",
                "imagem_url": "url",
                "cta": "chamada"
            }
        """
        print(f"🎨 Criando conteúdo para: {tema}")
        
        # 1. Gerar legenda com Gemini
        print("  📝 Gerando legenda...")
        conteudo = self.gemini.gerar_legenda(tema, tipo, tom)
        
        # 2. Revisar com Claude
        print("  🔍 Revisando com Claude...")
        legenda_revisada = self.claude.revisar_legenda(
            conteudo.get("legenda", ""),
            tema
        )
        conteudo["legenda"] = legenda_revisada
        
        # 3. Criar imagem com Canva
        print("  🎨 Criando imagem...")
        if tipo == "post":
            imagem_url = self.canva.criar_post(tema, legenda_revisada)
        elif tipo == "story":
            imagem_url = self.canva.criar_story(tema, legenda_revisada)
        elif tipo == "reel":
            imagem_url = self.canva.criar_reel_thumbnail(tema)
        else:
            imagem_url = self.canva.criar_post(tema, legenda_revisada)
        
        conteudo["imagem_url"] = imagem_url
        
        print(f"  ✅ Conteúdo criado com sucesso!")
        return conteudo
