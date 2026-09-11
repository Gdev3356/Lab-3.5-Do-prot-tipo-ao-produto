from typing import List, Dict, Any

PRECOS = {
    "pequeno": {"banho": 40.0, "tosa": 30.0, "corte_unhas": 15.0, "hidratacao": 25.0},
    "medio":   {"banho": 55.0, "tosa": 40.0, "corte_unhas": 15.0, "hidratacao": 35.0},
    "grande":  {"banho": 75.0, "tosa": 50.0, "corte_unhas": 20.0, "hidratacao": 45.0},
}

AGENDA_OCUPADA = [
    ("segunda", "tarde"),
    ("sexta", "tarde")
]

def calcular_orcamento(porte: str, servicos: List[str]) -> Dict[str, Any]:
    """Calcula o valor total estimado do agendamento com base no porte do pet e lista de serviços."""
    porte_clean = porte.lower().strip()
    if porte_clean not in PRECOS:
        return {"erro": f"Porte '{porte}' inválido. Use pequeno, medio ou grande."}

    total = 0.0
    detalhes = {}
    tabela = PRECOS[porte_clean]

    for s in servicos:
        s_clean = s.lower().strip()
        if s_clean in tabela:
            valor = tabela[s_clean]
            total += valor
            detalhes[s_clean] = valor
        else:
            encontrado = False
            for k, v in tabela.items():
                if k in s_clean or s_clean in k:
                    total += v
                    detalhes[k] = v
                    encontrado = True
                    break
            if not encontrado:
                detalhes[s_clean] = "Serviço não reconhecido"

    return {
        "porte": porte_clean,
        "servicos_calculados": detalhes,
        "valor_total": total
    }

def verificar_disponibilidade(dia: str, periodo: str) -> Dict[str, Any]:
    """Verifica a disponibilidade na agenda do pet shop para determinado dia e período."""
    dia_clean = dia.lower().strip()
    periodo_clean = periodo.lower().strip()

    esta_ocupado = any(d in dia_clean and p in periodo_clean for d, p in AGENDA_OCUPADA)

    if esta_ocupado:
        return {
            "disponivel": False,
            "mensagem": f"O período da {periodo_clean} na {dia_clean} está lotado.",
            "sugestoes": ["quarta à tarde", "quinta de manhã", "segunda de manhã"]
        }
    else:
        return {
            "disponivel": True,
            "mensagem": f"Horário disponível para {dia_clean} no período da {periodo_clean}."
        }

FUNCOES_DISPONIVEIS = {
    "calcular_orcamento": calcular_orcamento,
    "verificar_disponibilidade": verificar_disponibilidade
}

TOOLS_DECLARATION = [
    {
        "type": "function",
        "name": "calcular_orcamento",
        "description": "Calcula o valor total estimado do agendamento com base no porte do pet e lista de serviços.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "porte": {"type": "STRING", "description": "Porte do pet: pequeno, medio ou grande"},
                "servicos": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "Lista de serviços desejados (banho, tosa, corte_unhas, hidratacao)"
                }
            },
            "required": ["porte", "servicos"]
        }
    },
    {
        "type": "function",
        "name": "verificar_disponibilidade",
        "description": "Verifica a disponibilidade na agenda do pet shop para determinado dia e período.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "dia": {"type": "STRING", "description": "Dia da semana"},
                "periodo": {"type": "STRING", "description": "Período do dia: manha ou tarde"}
            },
            "required": ["dia", "periodo"]
        }
    }
]