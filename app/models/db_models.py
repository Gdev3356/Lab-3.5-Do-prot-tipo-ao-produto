from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SessionModel(Base):
    """Representa uma sessão contínua de atendimento ao cliente."""
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    last_interaction_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("MessageLogModel", back_populates="session")
    tool_logs = relationship("ToolLogModel", back_populates="session")
    agendamento = relationship("AgendamentoModel", back_populates="session", uselist=False)

class MessageLogModel(Base):
    """Armazena as mensagens trocadas entre Usuário e Assistente."""
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    role = Column(String, nullable=False) # 'user' ou 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("SessionModel", back_populates="messages")

class ToolLogModel(Base):
    """Auditoria de chamadas de ferramentas executadas pelo LLM."""
    __tablename__ = "tool_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    tool_name = Column(String, nullable=False)
    arguments_json = Column(Text, nullable=False)
    result_json = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("SessionModel", back_populates="tool_logs")

class AgendamentoModel(Base):
    """Ficha do agendamento finalizado persistido no BD."""
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), unique=True)
    nome_pet = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    porte = Column(String, nullable=False)
    servicos = Column(String, nullable=False) # Armazenado como string/JSON separado por vírgula
    dia = Column(String, nullable=False)
    periodo = Column(String, nullable=False)
    valor_total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("SessionModel", back_populates="agendamento")