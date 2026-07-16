import csv
import time
import schedule
from datetime import datetime
import os

class AgendaScheduler:
    def __init__(self):
        self.arquivo_agenda = "agenda.csv"
        self.carregar_agenda()
    
    def carregar_agenda(self):
        """Carrega agenda do CSV"""
        if os.path.exists(self.arquivo_agenda):
            self.agenda = []
            with open(self.arquivo_agenda, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row['publicado'] = row.get('publicado', 'False').strip().lower() == 'true'
                    self.agenda.append(row)
        else:
            self.agenda = []
            self.criar_agenda_exemplo()
    
    def criar_agenda_exemplo(self):
        """Cria agenda exemplo"""
        dados = [
            {"data": "2026-07-20", "hora": "10:00", "tema": "Lançamento Produto", "tipo": "post", "tom": "profissional", "publicado": False, "hashtags_personalizadas": ""},
            {"data": "2026-07-20", "hora": "15:00", "tema": "Promoção Especial", "tipo": "story", "tom": "promocional", "publicado": False, "hashtags_personalizadas": ""},
            {"data": "2026-07-21", "hora": "11:00", "tema": "Dicas de Beleza", "tipo": "reel", "tom": "divertido", "publicado": False, "hashtags_personalizadas": ""},
        ]
        self.agenda = dados
        self.salvar_agenda()
    
    def salvar_agenda(self):
        """Salva agenda atualizada"""
        fieldnames = ["data", "hora", "tema", "tipo", "tom", "hashtags_personalizadas", "publicado"]
        with open(self.arquivo_agenda, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for post in self.agenda:
                writer.writerow({
                    "data": post.get("data", ""),
                    "hora": post.get("hora", ""),
                    "tema": post.get("tema", ""),
                    "tipo": post.get("tipo", ""),
                    "tom": post.get("tom", ""),
                    "hashtags_personalizadas": post.get("hashtags_personalizadas", ""),
                    "publicado": str(post.get("publicado", False))
                })
    
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
            "publicado": False,
            "hashtags_personalizadas": ""
        }
        self.agenda.append(novo)
        self.salvar_agenda()
