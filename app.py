from flask import Flask, render_template_string, request, jsonify, redirect, url_for, session
from functools import wraps
from datetime import datetime

# Importações dos seus módulos locais
from config import SECRET_KEY, EMPREENDIMENTOS, USUARIOS
from templates import LOGIN_TEMPLATE, SISTEMA_TEMPLATE
from utils import (gerar_meses, carregar_dados, salvar_dados, 
                   calcular_saldo_acumulado_export)
from excel_generator import gerar_excel_fluxo

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ----------------------------------------------------------------
# DECORADORES (Segurança e Acesso)
# ----------------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login_page'))
        if session.get('usuario') != 'ADM':
            return jsonify({'success': False, 'error': 'Acesso restrito a administradores'}), 403
        return f(*args, **kwargs)
    return decorated_function

# ----------------------------------------------------------------
# ROTAS DE AUTENTICAÇÃO
# ----------------------------------------------------------------

@app.route('/')
@app.route('/login')
def login_page():
    if 'usuario' in session:
        return redirect(url_for('sistema_controle'))
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    usuario = data.get('usuario', '')
    senha = data.get('senha', '')
    
    if usuario in USUARIOS and USUARIOS[usuario]['senha'] == senha:
        session['usuario'] = usuario
        session['setor'] = USUARIOS[usuario]['setor']
        session['is_admin'] = (usuario == 'ADM')
        return jsonify({'success': True, 'redirect_url': '/sistema-controle'})
    
    return jsonify({'success': False, 'message': 'Usuário ou senha incorretos'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# ----------------------------------------------------------------
# ROTAS DO SISTEMA (Páginas e API)
# ----------------------------------------------------------------

@app.route('/sistema-controle')
@login_required
def sistema_controle():
    dados, meses, saldos_iniciais = carregar_dados()
    if not meses: meses = gerar_meses()
    if not saldos_iniciais:
        saldos_iniciais = {emp: 0 for emp in EMPREENDIMENTOS}
    
    return render_template_string(
        SISTEMA_TEMPLATE, 
        usuario=session['usuario'],
        setor=session['setor'],
        is_admin=session.get('is_admin', False),
        empreendimentos=EMPREENDIMENTOS,
        saldos_iniciais=saldos_iniciais
    )

@app.route('/api/dados')
@login_required
def api_dados():
    dados, meses, saldos_iniciais = carregar_dados()
    return jsonify({
        'success': True,
        'dados': dados,
        'meses': meses,
        'saldos_iniciais': saldos_iniciais
    })

@app.route('/api/atualizar-entrada', methods=['POST'])
@login_required
def api_atualizar_entrada():
    try:
        data = request.get_json()
        mes = data.get('mes')
        empreendimento = data.get('empreendimento')
        entrada = float(data.get('entrada', 0))
        
        if not mes or not empreendimento:
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400
        
        dados, meses, saldos_iniciais = carregar_dados()
        index = next((i for i, d in enumerate(dados) if d['mes'] == mes and d['empreendimento'] == empreendimento), -1)
        
        registro = {
            'mes': mes,
            'empreendimento': empreendimento,
            'entrada': entrada,
            'usuario': session.get('usuario'),
            'data_atualizacao': datetime.now().isoformat()
        }
        
        if index >= 0:
            dados[index] = registro
        else:
            dados.append(registro)
            
        salvar_dados(dados, meses, saldos_iniciais)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/atualizar-saldo', methods=['POST'])
@admin_required
def api_atualizar_saldo():
    try:
        data = request.get_json()
        empreendimento = data.get('empreendimento')
        saldo = float(data.get('saldo', 0))
        
        dados, meses, saldos_iniciais = carregar_dados()
        saldos_iniciais[empreendimento] = saldo
        salvar_dados(dados, meses, saldos_iniciais)
        
        return jsonify({'success': True, 'saldos': saldos_iniciais})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/atualizar-saldos', methods=['POST'])
@admin_required
def api_atualizar_saldos():
    try:
        data = request.get_json()
        novos_saldos = data.get('saldos', {})
        dados, meses, saldos_iniciais = carregar_dados()
        
        for emp, saldo in novos_saldos.items():
            if emp in EMPREENDIMENTOS:
                saldos_iniciais[emp] = float(saldo)
                
        salvar_dados(dados, meses, saldos_iniciais)
        return jsonify({'success': True, 'saldos': saldos_iniciais})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/validar-dados', methods=['POST'])
@login_required
def api_validar_dados():
    try:
        dados, meses, saldos_iniciais = carregar_dados()
        erros = []
        for d in dados:
            if d.get('entrada', 0) < 0:
                erros.append(f"Entrada negativa em {d['mes']} - {d['empreendimento']}")
        return jsonify({'success': True, 'erros': erros})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/limpar-tudo', methods=['POST'])
@admin_required
def api_limpar_tudo():
    try:
        meses = gerar_meses()
        saldos_iniciais = {emp: 0 for emp in EMPREENDIMENTOS}
        salvar_dados([], meses, saldos_iniciais)
        return jsonify({'success': True, 'saldos_iniciais': saldos_iniciais})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/carregar-template', methods=['POST'])
@login_required
def api_carregar_template():
    try:
        meses = gerar_meses()
        saldos_iniciais = {emp: 0 for emp in EMPREENDIMENTOS}
        salvar_dados([], meses, saldos_iniciais)
        return jsonify({'success': True, 'meses': meses, 'saldos_iniciais': saldos_iniciais})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ----------------------------------------------------------------
# ROTA DE EXPORTAÇÃO (Modularizada)
# ----------------------------------------------------------------

@app.route('/api/exportar-excel-completo')
@login_required
def api_exportar_excel_completo():
    try:
        dados, meses, saldos_iniciais = carregar_dados()
        usuario_nome = session.get('usuario', 'N/A')
        
        # Chama a função do módulo excel_generator.py
        excel_binario = gerar_excel_fluxo(dados, meses, saldos_iniciais, usuario_nome)
        
        data_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        return excel_binario, 200, {
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Content-Disposition': f'attachment; filename="Fluxo_Caixa_Projetado_{data_str}.xlsx"'
        }
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ----------------------------------------------------------------
# EXECUÇÃO DO SERVIDOR
# ----------------------------------------------------------------

if __name__ == '__main__':
    # Garante que o arquivo de dados exista na primeira execução
    d, m, s = carregar_dados()
    if not m:
        salvar_dados([], gerar_meses(), {emp: 0 for emp in EMPREENDIMENTOS})
        print("📁 Arquivo de dados inicializado.")

    print(f"🚀 Servidor rodando em http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)