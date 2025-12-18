import uvicorn
import webbrowser
import sys
import os
from threading import Timer
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
import platform

# Importação da lógica do seu projeto
from services import CashFlowService
from model import CashFlowModel

app = FastAPI(title="Projetado - INCORPORAÇÃO")

# Configuração de CORS para evitar bloqueios do navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def resource_path(relative_path):
    """ Encontra o caminho do arquivo para rodar como script ou no .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- ROTAS DE INTERFACE (FRONT-END) ---

@app.get("/", include_in_schema=False)
async def get_index():
    return FileResponse(resource_path('index.html'))

@app.get("/app.js", include_in_schema=False)
async def get_javascript():
    return FileResponse(resource_path('app.js'))

@app.get("/main.css", include_in_schema=False)
async def get_css():
    return FileResponse(resource_path('main.css'))

# --- ROTAS DA API (CORRIGIDAS PARA O APP.JS) ---

@app.get("/api/health")
async def health_check():
    """Resolve o status 'Offline' no rodapé"""
    return {"status": "ok", "message": "API Online"}

@app.get("/api/template")
async def get_template():
    """Resolve o erro 'Error loading template'"""
    try:
        # Usa o serviço para pegar o template formatado
        data = CashFlowService.get_template()
        return {
            "status": "sucesso",
            "data": data
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "erro", "message": str(e)}
        )

@app.post("/api/validate")
async def validate_data(request: Request):
    """Rota para o botão Validar Dados"""
    try:
        payload = await request.json()
        # O app.js envia os dados dentro de 'data'
        result = CashFlowService.validate_data(payload.get('data', []))
        return {
            "status": "sucesso",
            "valid": result['valid'],
            "errors": result['errors'],
            "data": result['data']
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "erro", "message": str(e)}
        )

@app.post("/api/export")
async def export_excel(request: Request):
    """Rota para o botão Exportar Excel"""
    try:
        payload = await request.json()
        output = CashFlowService.generate_excel(payload.get('data', []))
        
        headers = {
            'Content-Disposition': 'attachment; filename="fluxo_caixa_projetado.xlsx"'
        }
        return StreamingResponse(
            output, 
            headers=headers, 
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "erro", "message": str(e)}
        )

# --- INICIALIZAÇÃO ---

def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("🚀 Sistema de Fluxo de Caixa Iniciado")
    print("📍 Disponível em http://127.0.0.1:8000")
    Timer(1.5, open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)