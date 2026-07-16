#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sistema de Automação Total para Instagram
Usa Gemini + Claude + Canva + Instagram APIs
100% automático, sem intervenção manual
"""

import time
import logging
import sys
from datetime import datetime
from config.api_config import APIConfig
from criacao.orquestrador import OrquestradorConteudo
from publicador.instagram_publisher import InstagramPublisher
from agendador.scheduler import AgendaScheduler

# Forçar saída UTF-8 no Windows PowerShell/Terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Configurar logs
logging.basicConfig(
    level=getattr(logging, APIConfig.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automacao.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class AutomacaoInstagram:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.orquestrador = OrquestradorConteudo()
        self.publicador = InstagramPublisher()
        self.scheduler = AgendaScheduler()
        
        self.logger.info("=" * 60)
        self.logger.info("🤖 AUTOMAÇÃO TOTAL DO INSTAGRAM INICIADA")
        self.logger.info("=" * 60)
        self.logger.info(f"📅 Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.logger.info(f"📊 Postagens agendadas: {len(self.scheduler.agenda)}")
        self.logger.info("=" * 60)
    
    def processar_proximo_post(self):
        """Processa o próximo post da agenda"""
        post = self.scheduler.get_proximo_post()
        
        if not post:
            self.logger.info("📋 Nenhum post pendente no momento.")
            return False
        
        self.logger.info(f"🚀 Processando post: {post['tema']}")
        self.logger.info(f"   Data: {post['data']} {post['hora']}")
        self.logger.info(f"   Tipo: {post['tipo']}")
        self.logger.info(f"   Tom: {post['tom']}")
        
        try:
            # 1. Criar conteúdo
            self.logger.info("  📝 Criando conteúdo...")
            conteudo = self.orquestrador.criar_conteudo_completo(
                tema=post['tema'],
                tipo=post['tipo'],
                tom=post['tom']
            )
            
            if not conteudo:
                self.logger.error("❌ Falha ao criar conteúdo")
                return False
            
            # 2. Publicar
            self.logger.info("  📤 Publicando...")
            
            if post['tipo'] == 'post':
                sucesso = self.publicador.publicar_post(
                    conteudo['imagem_url'],
                    conteudo['legenda'] + "\n\n" + conteudo.get('hashtags', '')
                )
            elif post['tipo'] == 'story':
                sucesso = self.publicador.publicar_story(
                    conteudo['imagem_url'],
                    conteudo['legenda'][:100]
                )
            elif post['tipo'] == 'reel':
                # Para reel, precisamos de vídeo
                # Usando imagem como fallback
                sucesso = self.publicador.publicar_reel(
                    conteudo['imagem_url'],
                    conteudo['legenda']
                )
            else:
                sucesso = False
            
            if sucesso:
                self.scheduler.marcar_publicado(post)
                self.logger.info(f"✅ Post publicado com sucesso: {post['tema']}")
                return True
            else:
                self.logger.error(f"❌ Falha ao publicar: {post['tema']}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar post: {e}")
            return False
    
    def executar_loop(self):
        """Loop principal de execução"""
        self.logger.info("🔄 Iniciando loop de monitoramento...")
        
        while True:
            try:
                # Verificar próximo post
                if self.processar_proximo_post():
                    self.logger.info("⏳ Aguardando próximo post...")
                else:
                    self.logger.info("💤 Sem postagens pendentes. Verificando novamente...")
                
                # Aguardar antes da próxima verificação
                time.sleep(APIConfig.VERIFICAR_INTERVALO)
                
            except KeyboardInterrupt:
                self.logger.info("👋 Sistema interrompido pelo usuário")
                break
            except Exception as e:
                self.logger.error(f"❌ Erro no loop: {e}")
                time.sleep(60)  # Esperar 1 minuto e tentar novamente
    
    def adicionar_post_manual(self):
        """Adiciona post manualmente (para testes)"""
        print("\n📝 ADICIONAR POSTAGEM MANUAL")
        print("-" * 40)
        
        data = input("📅 Data (YYYY-MM-DD): ")
        hora = input("🕐 Hora (HH:MM): ")
        tema = input("📌 Tema: ")
        tipo = input("📂 Tipo (post/story/reel): ")
        tom = input("🎭 Tom (profissional/promocional/divertido/emocional): ")
        
        self.scheduler.adicionar_post(data, hora, tema, tipo, tom)
        print(f"✅ Postagem agendada para {data} às {hora}!")

if __name__ == "__main__":
    # Validar configurações
    try:
        APIConfig.validar()
    except Exception as e:
        print(f"❌ {e}")
        exit(1)
    
    # Criar pasta de logs
    import os
    os.makedirs("logs", exist_ok=True)
    
    # Iniciar sistema
    sistema = AutomacaoInstagram()
    
    # Menu
    print("\n" + "=" * 50)
    print("🤖 AUTOMAÇÃO TOTAL DO INSTAGRAM")
    print("=" * 50)
    print("1. 🚀 Iniciar modo automático (24/7)")
    print("2. 📝 Adicionar postagem manual")
    print("3. 📋 Ver agenda")
    print("4. ⚙️ Processar postagens pendentes agora")
    print("5. ❌ Sair")
    print("=" * 50)
    
    opcao = input("Escolha: ")
    
    if opcao == "1":
        sistema.executar_loop()
    elif opcao == "2":
        sistema.adicionar_post_manual()
    elif opcao == "3":
        print("\n📋 AGENDA:")
        for p in sistema.scheduler.agenda:
            status = "✅" if p.get("publicado") else "⏳"
            print(f"{status} {p['data']} {p['hora']} - {p['tema']} ({p['tipo']})")
    elif opcao == "4":
        sistema.processar_proximo_post()
    elif opcao == "5":
        print("👋 Até logo!")
    else:
        print("❌ Opção inválida!")
