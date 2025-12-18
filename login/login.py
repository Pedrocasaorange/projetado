from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from functools import wraps
import os

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.secret_key = 'Chave_segurança'  # Mude para uma chave segura

# Dicionário de usuários e seus setores
USUARIOS = {
    'Legalização': {'senha': 'legalização2025', 'setor': 'legalizacao'},
    'obra': {'senha': 'Obra2025', 'setor': 'obra'},
    'Projetos': {'senha': 'Projetos2025', 'setor': 'projeto'},
    'marketing': {'senha': 'Marketing2025', 'setor': 'marketing'},
    'Produtos': {'senha': 'Produtos2025', 'setor': 'Marketing'},
    'Pos obra': {'senha': 'Pos-obra2025', 'setor': 'Pos obra'},
    'ADM': {'senha': 'C2025asaOrange', 'setor': 'Adiministrador'}
}

# Decorator para verificar se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@app.route('/login')
def login_page():
    # Se já estiver logado, redireciona para o painel
    if 'usuario' in session:
        setor = session.get('setor', '')
        return redirect(url_for('painel', setor=setor))
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    usuario = data.get('usuario', '')
    senha = data.get('senha', '')
    
    if usuario in USUARIOS and USUARIOS[usuario]['senha'] == senha:
        session['usuario'] = usuario
        session['setor'] = USUARIOS[usuario]['setor']
        
        # Define a URL de redirecionamento baseada no setor
        redirect_url = f"/painel/{session['setor']}"
        
        return jsonify({
            'success': True,
            'redirect_url': redirect_url
        })
    
    return jsonify({
        'success': False,
        'message': 'Usuário ou senha incorretos'
    }), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/painel/<setor>')
@login_required
def painel(setor):
    if 'usuario' not in session:
        return redirect(url_for('login_page'))
    
    # Verifica se o setor na URL corresponde ao da sessão
    if session.get('setor') != setor:
        return redirect(url_for('painel', setor=session.get('setor')))
    
    # Mapeamento de títulos para cada setor
    titulos_setor = {
        'legalizacao': 'Painel de Legalização',
        'obra': 'Painel de Gestão de Obras',
        'projeto': 'Painel de Gerenciamento de Projetos',
        'marketing': 'Painel de Marketing'
    }
    
    titulo = titulos_setor.get(setor, 'Painel do Usuário')
    usuario = session['usuario']
    
    return render_template('painel.html', 
                         titulo=titulo, 
                         usuario=usuario, 
                         setor=setor.capitalize())

if __name__ == '__main__':
    # Configuração para rodar localmente
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )