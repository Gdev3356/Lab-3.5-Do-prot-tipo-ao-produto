import uuid
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import engine, get_db, Base
from app.models.db_models import SessionModel, MessageLogModel, AgendamentoModel
from app.schemas.pydantic_schemas import ChatRequest, ChatResponse, AgendamentoOut
from app.services.assistant import processar_interacao_assistente

# Cria as tabelas na inicialização
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pet Shop PetTech - AuAu Assistant API",
    description="API para atendimento automatizado e agendamento pet via Gemini AI",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/chat", response_model=ChatResponse, summary="Enviar mensagem ao assistente")
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. Recupera ou cria uma nova sessão
    session_id = request.session_id or str(uuid.uuid4())
    session_db = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session_db:
        session_db = SessionModel(id=session_id)
        db.add(session_db)
        db.commit()

    # 2. Salva a mensagem do usuário
    msg_user = MessageLogModel(session_id=session_id, role="user", content=request.message)
    db.add(msg_user)
    db.commit()

    # 3. Executa a inteligência do assistente (parâmetros alinhados com assistant.py)
    resposta_texto, nova_interaction_id, ficha = processar_interacao_assistente(
        user_prompt=request.message,
        db=db,
        previous_interaction_id=session_db.last_interaction_id
    )

    # 4. Atualiza a sessão e salva a resposta
    session_db.last_interaction_id = nova_interaction_id
    msg_assistant = MessageLogModel(session_id=session_id, role="assistant", content=resposta_texto)
    db.add(msg_assistant)
    db.commit()

    return ChatResponse(
        session_id=session_id,
        interaction_id=nova_interaction_id,
        response=resposta_texto,
        ficha_agendamento=ficha
    )

@app.get("/api/v1/agendamentos", response_model=List[AgendamentoOut], summary="Listar agendamentos salvos")
def listar_agendamentos(db: Session = Depends(get_db)):
    return db.query(AgendamentoModel).all()

@app.get("/api/v1/sessions/{session_id}/history", summary="Obter histórico de conversa")
def historico_sessao(session_id: str, db: Session = Depends(get_db)):
    session_db = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session_db:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    mensagens = db.query(MessageLogModel).filter(MessageLogModel.session_id == session_id).all()
    return {
        "session_id": session_id,
        "messages": [{"role": m.role, "content": m.content, "timestamp": m.timestamp} for m in mensagens]
    }

frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def read_index():
        return FileResponse(os.path.join(frontend_path, "index.html"))