import json
import os

DATA_FILE = 'fluxo_caixa_dados.json'

def gerar_meses():
    meses = []
    for ano in range(2025, 2031):
        # Regra: 2025 começa em Nov, 2030 termina em Dez
        inicio = 11 if ano == 2025 else 1
        fim = 13
        nomes = ['', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
        for i in range(inicio, fim):
            meses.append(f"{nomes[i]}/{str(ano)[2:]}")
    return meses

def carregar_dados():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Garante que saldos_iniciais seja um dicionário
                return data.get('dados', []), data.get('meses', gerar_meses()), data.get('saldos_iniciais', {})
        except:
            return [], gerar_meses(), {}
    return [], gerar_meses(), {}

def salvar_dados(dados, meses, saldos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'dados': dados, 
            'meses': meses, 
            'saldos_iniciais': saldos
        }, f, indent=2, ensure_ascii=False)