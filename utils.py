import json
import os
from datetime import datetime
from flask import session
from config import DATA_FILE, EMPREENDIMENTOS

def gerar_meses():
    meses = []
    anos = range(2025, 2031)
    nomes_meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 
                   'jul', 'ago', 'set', 'out', 'nov', 'dez']
    for ano in anos:
        for i, mes_nome in enumerate(nomes_meses, 1):
            if ano == 2025 and i < 11: continue
            if ano == 2030 and i > 12: break
            meses.append(f"{mes_nome}/{str(ano)[2:]}")
    return meses

def carregar_dados():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('dados', []), data.get('meses', gerar_meses()), data.get('saldos_iniciais', {})
        except:
            return [], gerar_meses(), {}
    return [], gerar_meses(), {}

def salvar_dados(dados, meses, saldos_iniciais):
    data = {
        'dados': dados,
        'meses': meses,
        'saldos_iniciais': saldos_iniciais,
        'ultima_atualizacao': datetime.now().isoformat(),
        'usuario_ultima_alteracao': session.get('usuario', 'desconhecido')
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def calcular_saldo_acumulado_export(mes, empreendimento, dados, meses, saldos_iniciais):
    saldo = saldos_iniciais.get(empreendimento, 0)
    mes_index = meses.index(mes)
    for i in range(mes_index + 1):
        mes_atual = meses[i]
        dados_mes = next((d for d in dados if d['mes'] == mes_atual and d['empreendimento'] == empreendimento), None)
        if dados_mes:
            saldo -= dados_mes.get('entrada', 0)
    return saldo