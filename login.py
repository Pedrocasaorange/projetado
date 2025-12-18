from flask import Flask, request, jsonify

app = Flask(__name__)

# Dados diretos
users = {
    "Legalização": "123",
    "obra": "123", 
    "Projeto": "123",
    "produtos": "123",
    "pos obra": "123",
    "marketing": "123",
    "adm": '123'
}

@app.route('/auth', methods=['POST'])
def auth():
    dados = request.json
    
    usuario = dados.get('usuario', '')
    senha = dados.get('senha', '')
    
    if usuario in users and users[usuario] == senha:
        return jsonify({
            "ok": True,
            "redirect": f"/painel/{usuario}",
            "usuario": usuario
        })
    
    return jsonify({"ok": False}), 401

@app.route('/painel/<usuario>', methods=['GET'])
def painel(usuario):
    if usuario not in users:
        return jsonify({"erro": "não existe"}), 404
    
    return jsonify({
        "usuario": usuario,
        "mensagem": f"Olá {usuario}"
    })

@app.route('/')
def inicio():
    return "Servidor rodando. Use /auth para login."

if __name__ == '__main__':
    app.run(port=5000)