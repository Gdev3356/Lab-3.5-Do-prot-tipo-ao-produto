import ssl
import warnings
import httpx
import os
import time
import random

warnings.filterwarnings("ignore")
ssl._create_default_https_context = ssl._create_unverified_context

# Configuração HTTPX estendida para suportar latência alta
_timeout_config = httpx.Timeout(90.0, connect=30.0)

_original_init = httpx.Client.__init__
def _patched_init(self, *args, **kwargs):
    kwargs["verify"] = False
    kwargs["timeout"] = _timeout_config
    _original_init(self, *args, **kwargs)
httpx.Client.__init__ = _patched_init

_original_async_init = httpx.AsyncClient.__init__
def _patched_async_init(self, *args, **kwargs):
    kwargs["verify"] = False
    kwargs["timeout"] = _timeout_config
    _original_async_init(self, *args, **kwargs)
httpx.AsyncClient.__init__ = _patched_async_init

from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=api_key) if api_key else genai.Client()
except Exception as e:
    print(f"[ERRO INICIALIZAÇÃO CLIENTE]: {e}")
    client = None

def processar_interacao_assistente(
    user_prompt: str,
    db: Optional[Session] = None,
    previous_interaction_id: Optional[str] = None
) -> Tuple[str, Optional[str], Dict[str, Any]]:
    
    print(f"\n---> [REQ RECEBIDA]: '{user_prompt}'")

    ficha = {
        "nome_pet": None,
        "especie": None,
        "porte": None,
        "servicos": [],
        "dia": None,
        "periodo": None,
        "valor_total": 0.0
    }

    if not client:
        return "Erro: Cliente Gemini não inicializado. Verifique a chave GEMINI_API_KEY.", None, ficha

    # Lista de modelos para fallback em ordem de prioridade
    modelos_candidatos = ["gemini-3.6-flash", "gemini-2.5-flash", "gemini-2.0-flash"]
    resposta_texto = None

    for modelo in modelos_candidatos:
        print(f"[TESTANDO MODELO]: {modelo}")
        
        for tentativa in range(1, 4):
            try:
                chat = client.chats.create(model=modelo)
                response = chat.send_message(user_prompt)
                resposta_texto = response.text or "Sem resposta gerada."
                print(f"---> [RESPOSTA OK ({modelo})]: {resposta_texto[:50]}...")
                break
            except Exception as e:
                erro_str = str(e)
                print(f"[TENTATIVA {tentativa}/3 FALHOU - {modelo}]: {erro_str}")
                
                # Se o modelo não existir (404), pula imediatamente para o próximo modelo da lista
                if "404" in erro_str or "NOT_FOUND" in erro_str:
                    break
                
                # Se for erro de sobrecarga (503 ou 429), aguarda tempo progressivo com variação aleatória
                if "503" in erro_str or "UNAVAILABLE" in erro_str or "429" in erro_str:
                    tempo_espera = (tentativa * 3) + random.uniform(1.0, 2.5)
                    print(f"[RETRY]: Servidor sobrecarregado. Aguardando {tempo_espera:.1f}s...")
                    time.sleep(tempo_espera)
                else:
                    break
        
        # Se conseguiu obter resposta em qualquer tentativa, encerra a busca
        if resposta_texto:
            break

    if not resposta_texto:
        resposta_texto = "O servidor do Gemini está enfrentando alto tráfego no momento. Aguarde cerca de 10 segundos e reenvie sua mensagem."

    return resposta_texto, None, ficha