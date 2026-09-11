from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class FichaAgendamento(BaseModel):
    nome_pet: Optional[str] = None
    especie: Optional[str] = None
    porte: Optional[str] = None
    servicos: Optional[List[str]] = None
    dia: Optional[str] = None
    periodo: Optional[str] = None
    valor_total: Optional[float] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    interaction_id: Optional[str] = None
    response: str
    ficha_agendamento: Optional[FichaAgendamento] = None

class AgendamentoOut(BaseModel):
    id: int
    session_id: str
    nome_pet: Optional[str] = None
    especie: Optional[str] = None
    porte: Optional[str] = None
    servicos: Optional[str] = None
    dia: Optional[str] = None
    periodo: Optional[str] = None
    valor_total: Optional[float] = None

    class Config:
        from_attributes = True