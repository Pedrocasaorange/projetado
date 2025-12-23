from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from functools import wraps
from config import SECRET_KEY, EMPREENDIMENTOS, USUARIOS
from templates import LOGIN_TEMPLATE, SISTEMA_TEMPLATE
from utils import carregar_dados, salvar_dados
from excel_generator import gerar_excel

app = Flask(__name__)
app.secret_key = SECRET_KEY

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session: return redirect('/login')
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index(): return redirect('/login')

@app.route('/login')
def login(): return render_template_string(LOGIN_TEMPLATE)

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    u = data.get('usuario')
    if u in USUARIOS and USUARIOS[u]['senha'] == data.get('senha'):
        session['usuario'] = u
        session['setor'] = USUARIOS[u]['setor']
        session['is_admin'] = (u == 'ADM')
        return jsonify({'success': True, 'redirect_url': '/sistema'})
    return jsonify({'success': False})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/sistema')
@login_required
def sistema():
    return render_template_string(SISTEMA_TEMPLATE, 
                                  is_admin=session['is_admin'],
                                  setor=session['setor'],
                                  empreendimentos=EMPREENDIMENTOS)

@app.route('/api/dados')
@login_required
def api_dados():
    todos_dados, meses, saldos = carregar_dados()
    
    # Determina qual setor filtrar
    req_setor = request.args.get('setor')
    setor_alvo = req_setor if session['is_admin'] and req_setor else session['setor']
    
    # Filtra dados do array principal
    dados_filtrados = [d for d in todos_dados if d.get('setor') == setor_alvo]
    
    return jsonify({
        'success': True,
        'dados': dados_filtrados,
        'meses': meses,
        'saldos_iniciais': saldos, # Envia tudo, o front filtra o setor
        'setor_atual': setor_alvo
    })

@app.route('/api/atualizar', methods=['POST'])
@login_required
def api_atualizar():
    data = request.json
    todos_dados, meses, saldos = carregar_dados()
    
    setor_alvo = data.get('setor') if session['is_admin'] and data.get('setor') else session['setor']
    
    # Atualiza entrada
    todos_dados = [d for d in todos_dados if not (
        d['mes'] == data['mes'] and 
        d['empreendimento'] == data['empreendimento'] and 
        d.get('setor') == setor_alvo
    )]
    todos_dados.append({
        'mes': data['mes'],
        'empreendimento': data['empreendimento'],
        'entrada': data['entrada'],
        'setor': setor_alvo
    })
    
    salvar_dados(todos_dados, meses, saldos)
    return jsonify({'success': True})

@app.route('/api/atualizar-saldo-inicial', methods=['POST'])
@login_required
def api_atualizar_saldo_inicial():
    if not session['is_admin']: return jsonify({'success': False}), 403
    
    data = request.json
    emp = data.get('empreendimento')
    valor = data.get('saldo')
    setor_alvo = data.get('setor')
    
    todos_dados, meses, saldos = carregar_dados()
    
    # Garante estrutura: saldos = { "obra": { "ALLEGRO": 100 }, ... }
    if setor_alvo not in saldos:
        saldos[setor_alvo] = {}
    
    saldos[setor_alvo][emp] = valor
    
    salvar_dados(todos_dados, meses, saldos)
    return jsonify({'success': True})

@app.route('/api/exportar')
@login_required
def api_exportar():
    req_setor = request.args.get('setor')
    setor_alvo = req_setor if session['is_admin'] and req_setor else session['setor']
    
    todos_dados, meses, saldos = carregar_dados()
    dados_filtrados = [d for d in todos_dados if d.get('setor') == setor_alvo]
    
    # Pega saldos específicos desse setor
    saldos_setor = saldos.get(setor_alvo, {})
    
    excel_file = gerar_excel(dados_filtrados, meses, saldos_setor, setor_alvo, EMPREENDIMENTOS)
    
    return excel_file, 200, {
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'Content-Disposition': f'attachment; filename=Fluxo_{setor_alvo}.xlsx'
    }

if __name__ == '__main__':
    carregar_dados()
    app.run(debug=True, port=5000)