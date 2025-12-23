LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Login Projetado</title>
    <style>
        body { display: flex; justify-content: center; align-items: center; height: 100vh; background: #f4f6f8; font-family: 'Segoe UI', sans-serif; }
        .box { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); width: 320px; text-align: center; }
        .logo-text { color: #FF6600; font-weight: 800; font-size: 24px; margin-bottom: 5px; }
        .sub-text { color: #888; font-size: 12px; margin-bottom: 25px; letter-spacing: 1px; }
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #e0e0e0; border-radius: 6px; box-sizing: border-box; background: #fafafa; transition: 0.3s; }
        input:focus { border-color: #FF6600; background: white; outline: none; }
        button { width: 100%; padding: 12px; background: #FF6600; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 14px; margin-top: 10px; transition: 0.2s; }
        button:hover { background: #e65c00; transform: translateY(-1px); }
    </style>
</head>
<body>
    <div class="box">
        <div class="logo-text">Projetado</div>
        <div class="sub-text">INCORPORAÇÃO</div>
        <input type="text" id="usuario" placeholder="Usuário">
        <input type="password" id="senha" placeholder="Senha">
        <button onclick="login()">ACESSAR SISTEMA</button>
    </div>
    <script>
        async function login() {
            const u = document.getElementById('usuario').value;
            const s = document.getElementById('senha').value;
            const res = await fetch('/auth', {
                method: 'POST', 
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({usuario: u, senha: s})
            });
            const data = await res.json();
            if(data.success) window.location.href = data.redirect_url;
            else alert('Credenciais inválidas');
        }
    </script>
</body>
</html>
'''

SISTEMA_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Projetado INCORPORAÇÃO</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #FF6600;
            --primary-light: #FFF3E0;
            --text-dark: #1a1a1a;
            --text-gray: #666;
            --bg-body: #F4F6F8;
            --border-color: #E0E0E0;
            --green-text: #00C853;
            --green-bg: #E8F5E9;
            --red-text: #D50000;
            --red-bg: #FFEBEE;
        }

        body { font-family: 'Inter', sans-serif; margin: 0; padding: 0; background: var(--bg-body); color: var(--text-dark); }
        
        /* --- HEADER --- */
        .header { background: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
        .logo-area { display: flex; align-items: center; gap: 10px; }
        .logo-icon { width: 35px; height: 35px; background: var(--primary); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px; }
        .logo-titles h1 { margin: 0; font-size: 18px; font-weight: 700; color: var(--text-dark); }
        .logo-titles span { font-size: 11px; color: #888; letter-spacing: 0.5px; text-transform: uppercase; font-weight: 600; }
        
        .user-area { display: flex; align-items: center; gap: 15px; }
        .badge-setor { background: var(--primary-light); color: var(--primary); padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        .btn-logout { background: transparent; border: 1px solid #ddd; padding: 6px 16px; border-radius: 6px; font-size: 13px; cursor: pointer; color: #555; transition: 0.2s; display: flex; align-items: center; gap: 5px; }
        .btn-logout:hover { background: #f5f5f5; color: #333; border-color: #ccc; }

        /* --- CONTROLS --- */
        .main-content { padding: 20px 30px; }
        .card-controls { background: white; padding: 15px 20px; border-radius: 10px; display: flex; align-items: center; gap: 15px; margin-bottom: 20px; border: 1px solid #eaeaea; }
        
        .control-group { display: flex; align-items: center; gap: 10px; }
        label { font-size: 13px; font-weight: 600; color: #555; }
        select { padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-family: inherit; font-size: 13px; background: #fafafa; min-width: 150px; }
        
        .btn-action { padding: 8px 16px; border: none; border-radius: 6px; font-size: 13px; font-weight: 500; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: 0.2s; }
        .btn-refresh { background: #e0e0e0; color: #333; }
        .btn-refresh:hover { background: #d0d0d0; }
        .btn-excel { background: white; border: 1px solid #ddd; color: #333; }
        .btn-excel:hover { border-color: #bbb; background: #fafafa; }

        /* --- TABLE --- */
        .card-table { background: white; border-radius: 12px; border: 1px solid #eaeaea; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
        .table-wrapper { height: 70vh; overflow: auto; position: relative; }
        
        table { border-collapse: separate; border-spacing: 0; width: 100%; min-width: 1600px; }
        
        thead th { background: white; position: sticky; top: 0; z-index: 10; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #666; border-bottom: 1px solid #eee; border-right: 1px solid #f0f0f0; }
        
        /* Linha 1 do Header (Nomes dos Projetos) */
        .header-project { padding: 15px 10px; font-weight: 700; color: #333; background: #fafafa !important; font-size: 12px; border-bottom: 1px solid #e0e0e0; }
        
        /* Linha 2 do Header (Saldo/Entrada) */
        .header-sub { padding: 10px; font-weight: 600; background: white; }
        
        /* Coluna Fixa (Datas) */
        .col-date-header { position: sticky; left: 0; z-index: 20; background: #fafafa; border-right: 2px solid #eee; padding: 15px; text-align: left; width: 80px; }
        .col-date-body { position: sticky; left: 0; z-index: 15; background: white; border-right: 2px solid #eee; padding: 12px 15px; font-size: 13px; font-weight: 600; color: #333; text-align: left; }
        
        tbody td { padding: 8px 10px; border-bottom: 1px solid #f5f5f5; border-right: 1px solid #f9f9f9; text-align: center; font-size: 13px; }
        
        /* Estilos Específicos */
        .row-inicial { background-color: #FFF8E1 !important; } /* Cor creme para saldo inicial */
        .row-inicial td { border-bottom: 1px solid #FFE0B2; font-weight: 600; color: #333; padding-top: 15px; padding-bottom: 15px; }
        .row-inicial .col-date-body { background-color: #FFF8E1 !important; color: #E65100; text-transform: uppercase; font-size: 11px; letter-spacing: 1px; }

        /* Cores de Números */
        .val-pos { color: var(--green-text); font-weight: 500; background: rgba(0, 200, 83, 0.05); padding: 4px 8px; border-radius: 4px; display: inline-block; min-width: 80px; }
        .val-neg { color: var(--red-text); font-weight: 500; background: rgba(213, 0, 0, 0.05); padding: 4px 8px; border-radius: 4px; display: inline-block; min-width: 80px; }
        .val-neu { color: #999; }
        
        /* Inputs */
        .input-entrada { border: 1px solid transparent; background: transparent; text-align: center; width: 100%; font-family: inherit; font-size: 13px; color: #333; padding: 5px; border-radius: 4px; transition: 0.2s; }
        .input-entrada:hover { background: #f5f5f5; }
        .input-entrada:focus { border: 1px solid var(--primary); background: white; outline: none; box-shadow: 0 0 0 3px rgba(255, 102, 0, 0.1); }
        .input-changed { color: var(--primary); font-weight: 600; }
        
        .input-ini { border: 1px solid #ddd; background: white; padding: 6px; border-radius: 4px; width: 80px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    
    <header class="header">
        <div class="logo-area">
            <div class="logo-icon">P</div>
            <div class="logo-titles">
                <h1>Projetado</h1>
                <span>INCORPORAÇÃO</span>
            </div>
        </div>
        <div class="user-area">
            <div class="badge-setor" id="displaySetor">{{ setor.upper() }}</div>
            <button class="btn-logout" onclick="window.location.href='/logout'">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"></path></svg>
                Sair
            </button>
        </div>
    </header>

    <div class="main-content">
        <div class="card-controls">
            {% if is_admin %}
            <div class="control-group">
                <label>Visualizar Setor:</label>
                <select id="selectSetor" onchange="carregarDados()">
                    <option value="legalizacao">Legalização</option>
                    <option value="obra">Obra</option>
                    <option value="projeto">Projetos</option>
                    <option value="marketing">Marketing</option>
                    <option value="produtos">Produtos</option>
                    <option value="pos_obra">Pós Obra</option>
                </select>
            </div>
            {% endif %}
            
            <button class="btn-action btn-refresh" onclick="carregarDados()">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                Atualizar
            </button>
            <button class="btn-action btn-excel" onclick="exportarExcel()">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5.586a1 1 0 0 1 .707.293l5.414 5.414a1 1 0 0 1 .293.707V19a2 2 0 0 1-2 2z"></path></svg>
                Gerar Excel
            </button>
        </div>

        <div class="card-table">
            <div class="table-wrapper">
                <table id="tabelaFluxo">
                    <thead id="tHead"></thead>
                    <tbody id="tBody"></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const empreendimentos = {{ empreendimentos|tojson }};
        const isAdmin = {{ 'true' if is_admin else 'false' }};
        let dados = [];
        let meses = [];
        let saldosIniciais = {}; 

        async function carregarDados() {
            let setorQuery = "";
            if(isAdmin) {
                const sel = document.getElementById('selectSetor');
                setorQuery = sel ? sel.value : "";
            }

            const res = await fetch(`/api/dados?setor=${setorQuery}`);
            const json = await res.json();
            
            if(json.success) {
                dados = json.dados;
                meses = json.meses;
                saldosIniciais = json.saldos_iniciais || {};
                
                if(isAdmin && json.setor_atual) {
                    document.getElementById('displaySetor').innerText = json.setor_atual.toUpperCase();
                }
                
                renderizar(json.setor_atual);
            }
        }

        function renderizar(setorAtual) {
            const thead = document.getElementById('tHead');
            const tbody = document.getElementById('tBody');
            
            // --- HEADER (Dupla Linha) ---
            // Linha 1: Datas + Nomes dos Projetos
            let htmlHead = `<tr><th rowspan="2" class="col-date-header">Datas</th>`;
            empreendimentos.forEach(emp => {
                htmlHead += `<th colspan="2" class="header-project">${emp}</th>`;
            });
            htmlHead += `</tr>`;
            
            // Linha 2: Saldo | Entrada
            htmlHead += `<tr>`;
            empreendimentos.forEach(emp => {
                htmlHead += `<th class="header-sub">Saldo</th><th class="header-sub">Entrada</th>`;
            });
            htmlHead += `</tr>`;
            thead.innerHTML = htmlHead;

            // --- BODY ---
            
            // 1. Linha Especial: SALDO INICIAL
            let htmlBody = `<tr class="row-inicial"><td class="col-date-body">SALDO INICIAL</td>`;
            empreendimentos.forEach(emp => {
                let valInicial = 0;
                if (saldosIniciais[setorAtual] && saldosIniciais[setorAtual][emp]) {
                    valInicial = saldosIniciais[setorAtual][emp];
                }

                // Coluna Saldo (Visualização ou Edição ADM)
                if (isAdmin) {
                    htmlBody += `<td><input type="number" step="0.01" class="input-ini" 
                                value="${valInicial}" 
                                onchange="salvarSaldoInicial('${emp}', this.value)"></td>`;
                } else {
                    htmlBody += `<td><span class="val-pos" style="background:white; border:1px solid #ddd;">${formatMoney(valInicial)}</span></td>`;
                }
                // Coluna Entrada (Vazia na linha inicial)
                htmlBody += `<td><span style="color:#aaa">--</span></td>`; 
            });
            htmlBody += `</tr>`;

            // 2. Linhas dos Meses
            htmlBody += meses.map(mes => {
                let linha = `<tr><td class="col-date-body">${mes}</td>`;
                
                empreendimentos.forEach(emp => {
                    let entrada = dados.find(d => d.mes === mes && d.empreendimento === emp)?.entrada || 0;
                    let saldo = calcularSaldoVisual(mes, emp, setorAtual);
                    
                    // Formatação condicional do saldo
                    let classeSaldo = saldo < 0 ? 'val-neg' : (saldo > 0 ? 'val-pos' : 'val-neu');
                    let displaySaldo = formatMoney(saldo);

                    linha += `<td><span class="${classeSaldo}">${displaySaldo}</span></td>`;
                    
                    // Input de entrada
                    let classeInput = entrada != 0 ? 'input-entrada input-changed' : 'input-entrada';
                    linha += `<td><input type="text" class="${classeInput}" value="${formatInput(entrada)}" 
                             onfocus="this.select()"
                             onblur="salvarEntrada('${mes}', '${emp}', this.value)"></td>`;
                });
                return linha + `</tr>`;
            }).join('');
            
            tbody.innerHTML = htmlBody;
        }

        // Helpers de Formatação
        function formatMoney(val) {
            return val.toLocaleString('pt-BR', {minimumFractionDigits: 2});
        }
        
        function formatInput(val) {
            return val === 0 ? "0,00" : val.toLocaleString('pt-BR', {minimumFractionDigits: 2});
        }
        
        function parseInput(val) {
            // Converte "1.000,00" para 1000.00
            if(typeof val === 'number') return val;
            return parseFloat(val.replace(/\./g, '').replace(',', '.')) || 0;
        }

        function calcularSaldoVisual(mes, emp, setor) {
            let s = 0;
            if (saldosIniciais[setor] && saldosIniciais[setor][emp]) {
                s = saldosIniciais[setor][emp];
            }
            let idx = meses.indexOf(mes);
            for(let i=0; i<=idx; i++) {
                let ent = dados.find(d => d.mes === meses[i] && d.empreendimento === emp)?.entrada || 0;
                s -= ent;
            }
            return s;
        }

        async function salvarEntrada(mes, emp, valStr) {
            let val = parseInput(valStr);
            let setorAlvo = isAdmin ? document.getElementById('selectSetor').value : "";
            
            await fetch('/api/atualizar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ mes, empreendimento: emp, entrada: val, setor: setorAlvo })
            });
            carregarDados();
        }

        async function salvarSaldoInicial(emp, val) {
            let setorAlvo = document.getElementById('selectSetor').value;
            await fetch('/api/atualizar-saldo-inicial', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ empreendimento: emp, saldo: parseFloat(val), setor: setorAlvo })
            });
            carregarDados();
        }

        function exportarExcel() {
            let setorAlvo = isAdmin ? document.getElementById('selectSetor').value : "";
            window.location.href = `/api/exportar?setor=${setorAlvo}`;
        }

        window.onload = carregarDados;
    </script>
</body>
</html>
'''