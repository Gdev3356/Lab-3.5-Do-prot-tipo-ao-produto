# 🐾 AuAu Assistant API - Pet Shop PetTech

API RESTful desenvolvida em Python e FastAPI para automatizar o atendimento ao cliente, consulta de preços, verificação de disponibilidade de horários e agendamento de serviços estéticos caninos/felinos utilizando a API Gemini da Google com **Function Calling** e **Saídas Estruturadas**.

---

## 🏛️ Arquitetura e Decisões Técnicas

O projeto foi migrado de um notebook no Google Colab para uma arquitetura em camadas orientada a serviços:

```
petshop-assistant-api/
├── app/
│   ├── models/       # Mapeamento do Banco de Dados (ORM SQLAlchemy)
│   ├── schemas/      # Contratos de DTO/API e Schemas Pydantic para a IA
│   ├── services/     # Regras de Negócio (Tools) e Integração com SDK Gemini
│   ├── config.py     # Gestão de Variáveis de Ambiente (.env)
│   ├── database.py   # Gerenciamento da Conexão SQLite
│   └── main.py       # Endpoints FastAPI e Gerenciamento de Sessões
├── .env.example
├── requirements.txt
└── README.md
```

### Principais Decisões Técnicas:
1. **FastAPI**: Escolhido pela alta velocidade, tipagem estática nativa com Pydantic e geração automática da documentação Swagger UI.
2. **SQLite + SQLAlchemy**: Persistência de dados leve e portátil sem necessidade de conteinerização complexa. Permite manter o histórico da conversa, auditoria de chamadas de ferramentas e gravação permanente dos agendamentos confirmados.
3. **Gerenciamento de Contexto (`session_id`)**: A API armazena o `last_interaction_id` retornado pela Interactions API do Gemini, mantendo o histórico conversacional ativo entre requisições HTTP sem depender de estado em memória local.
4. **Guardrails & Segurança**:
   - As ferramentas permitidas ao LLM são estritamente delimitadas em um *dispatcher*.
   - Injeção de instrução de segurança (Guardrail Veterinário) recusa serviços estéticos se houver sintomas médicos relatados.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10 ou superior
- Chave de API do Google Gemini (`GEMINI_API_KEY`)

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/petshop-assistant-api.git](https://github.com/seu-usuario/petshop-assistant-api.git)
   cd petshop-assistant-api
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # Linux/macOS:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as Variáveis de Ambiente:**
   Crie um arquivo `.env` baseado no `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Edite o arquivo `.env` e adicione sua chave:
   ```env
   GEMINI_API_KEY="sua_chave_aqui"
   DATABASE_URL="sqlite:///./petshop.db"
   MODEL_NAME="gemini-3.6-flash"
   ```

5. **Inicie o servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Acesse a documentação:**
   Navegue até [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para interagir com os endpoints via Swagger.

---

## 📌 Endpoints Principais

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/api/v1/chat` | Envia uma mensagem e retorna a resposta do assistente (gerencia sessão) |
| `GET` | `/api/v1/agendamentos` | Lista todos os agendamentos confirmados e gravados no banco |
| `GET` | `/api/v1/sessions/{id}/history` | Exibe histórico completo de mensagens e auditoria de chamadas de ferramentas |

---

## 🛡️ Destaques de Testes e Segurança

- **Proteção contra Vazamento de Credenciais:** Arquivos sensíveis (`.env`, `petshop.db`) devidamente listados no `.gitignore`.
- **Testado para Sintomas Médicos:** Ao informar frases como *"Meu pet está vomitando e prostrado"*, o assistente aciona o guardrail de saúde e recusa o agendamento imediatamente.# Lab-3.5-Do-prot-tipo-ao-produto
