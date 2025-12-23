import io
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def gerar_excel(dados_filtrados, meses, saldos_iniciais_setor, nome_setor, lista_empreendimentos):
    wb = Workbook()
    ws = wb.active
    ws.title = f"Fluxo - {nome_setor}"
    
    font_bold = Font(bold=True)
    align_center = Alignment(horizontal="center", vertical="center")
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    # Cabeçalho Principal
    ws.merge_cells('A1:Q1')
    ws['A1'] = f"RELATÓRIO DE FLUXO - SETOR: {nome_setor.upper()}"
    ws['A1'].font = Font(size=14, bold=True, color="FFFFFF")
    ws['A1'].fill = PatternFill(start_color="FF6600", end_color="FF6600", fill_type="solid") # Cor Laranja
    ws['A1'].alignment = align_center

    # Cabeçalhos da Tabela
    ws['A3'] = "Datas"
    ws['A3'].font = font_bold
    ws['A3'].alignment = align_center
    
    col_idx = 2
    for emp in lista_empreendimentos:
        # Pega saldo inicial deste emp neste setor
        saldo_ini = saldos_iniciais_setor.get(emp, 0)
        
        c_saldo = ws.cell(row=3, column=col_idx, value=f"{emp}\nSaldo (Ini: {saldo_ini})")
        c_saldo.font = font_bold
        c_saldo.alignment = align_center
        c_saldo.border = border
        
        c_ent = ws.cell(row=3, column=col_idx+1, value=f"{emp}\nEntrada")
        c_ent.font = font_bold
        c_ent.alignment = align_center
        c_ent.border = border
        col_idx += 2

    # Preenchendo dados
    row_idx = 4
    for mes in meses:
        ws.cell(row=row_idx, column=1, value=mes).border = border
        
        col_idx = 2
        for emp in lista_empreendimentos:
            # 1. Calcular Saldo Acumulado
            saldo = saldos_iniciais_setor.get(emp, 0)
            
            # --- CORREÇÃO AQUI: (d.get('entrada') or 0) garante que nunca seja None ---
            mes_index = meses.index(mes)
            for i in range(mes_index + 1):
                mes_anterior = meses[i]
                ent_anterior = next(( (d.get('entrada') or 0) for d in dados_filtrados if d['mes'] == mes_anterior and d['empreendimento'] == emp), 0)
                saldo -= ent_anterior
            
            # 2. Pegar Entrada Atual
            entrada = next(( (d.get('entrada') or 0) for d in dados_filtrados if d['mes'] == mes and d['empreendimento'] == emp), 0)
            
            # Escrever células
            c_s = ws.cell(row=row_idx, column=col_idx, value=saldo)
            c_s.number_format = '#,##0.00'
            c_s.border = border
            
            # Formatação condicional simples no Excel (Vermelho se negativo, Verde se positivo)
            if saldo < 0:
                c_s.font = Font(color="D50000")
            elif saldo > 0:
                c_s.font = Font(color="00C853")
            
            c_e = ws.cell(row=row_idx, column=col_idx+1, value=entrada)
            c_e.number_format = '#,##0.00'
            c_e.border = border
            
            col_idx += 2
        row_idx += 1

    out = io.BytesIO()
    wb.save(out)
    out.seek(0)
    return out.getvalue()