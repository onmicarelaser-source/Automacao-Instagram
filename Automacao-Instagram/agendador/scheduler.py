import pandas as pd
import time
import schedule
from datetime import datetime, timedelta
import os

class AgendaScheduler:
    def __init__(self):
        self.arquivo_agenda = "agenda.csv"
        self.carregar_agenda()
    
    def carregar_agenda(self):
        """Carrega agenda do CSV"""
        if os.path.exists(self.arquivo_agenda):
            df = pd.read_csv(self.arquivo_agenda)
            self.agenda = df.to_dict('records')
        else:
            self.agenda = []
            self.criar_agenda_exemplo()
    
    def criar_agenda_exemplo(self):
        """Cria agenda exemplo"""
        dados = [
            {"data": "2026-07-20", "hora": "10:00", "tema": "Lançamento Produto", "tipo": "post", "tom": "profissional", "publicado": False},
            {"data": "2026-07-20", "hora": "15:00", "tema": "Promoção Especial", "tipo": "story", "tom": "promocional", "publicado": False},
            {"data": "2026-07-21", "hora": "11:00", "tema": "Dicas de Beleza", "tipo": "reel", "tom": "divertido", "publicado": False},
        ]
        df = pd.DataFrame(dados)
        df.to_csv(self.arquivo_agenda, index=False)
        self.agenda = dados
    
    def salvar_agenda(self):
        """Salva agenda atualizada"""
        df = pd.DataFrame(self.agenda)
        df.to_csv(self.arquivo_agenda, index=False)
    
    def get_proximo_post(self):
        """Retorna próximo post a ser publicado"""
        agora = datetime.now()
        
        for post in self.agenda:
            if post.get("publicado", False):
                continue
                
            data_hora = datetime.strptime(f"{post['data']} {post['hora']}", "%Y-%m-%d %H:%M")
            
            if data_hora <= agora:
                return post
        
        return None
    
    def marcar_publicado(self, post_id):
        """Marca post como publicado"""
        for post in self.agenda:
            if post["data"] == post_id["data"] and post["hora"] == post_id["hora"]:
                post["publicado"] = True
                break
        
        self.salvar_agenda()
    
    def adicionar_post(self, data, hora, tema, tipo, tom="profissional"):
        """Adiciona novo post à agenda"""
        novo = {
            "data": data,
            "hora": hora,
            "tema": tema,
            "tipo": tipo,
            "tom": tom,
            "publicado": False
        }
        self.agenda.append(novo)
        self.salvar_agenda()
