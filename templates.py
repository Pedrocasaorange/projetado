LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Projetado INCORPORAÇÃO</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .login-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
            padding: 40px;
        }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { color: #E65100; font-size: 32px; margin-bottom: 10px; }
        .logo p { color: #6b7280; font-size: 14px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; color: #374151; font-weight: 500; }
        .form-group input {
            width: 100%; padding: 12px 15px; border: 1px solid #d1d5db;
            border-radius: 8px; font-size: 16px; transition: all 0.3s ease;
        }
        .form-group input:focus {
            outline: none; border-color: #E65100; box-shadow: 0 0 0 3px rgba(230, 81, 0, 0.1);
        }
        .btn-login {
            width: 100%; padding: 14px; background: linear-gradient(135deg, #E65100 0%, #FF9800 100%);
            color: white; border: none; border-radius: 8px; font-size: 16px;
            font-weight: 600; cursor: pointer; transition: all 0.3s ease;
        }
        .btn-login:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(230, 81, 0, 0.2); }
        .error-message {
            background-color: #fee2e2; color: #991b1b; padding: 12px;
            border-radius: 8px; margin-bottom: 20px; text-align: center; display: none;
        }
        .footer { text-align: center; margin-top: 30px; color: #6b7280; font-size: 14px; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1>Projetado INCORPORAÇÃO</h1>
            <p>Sistema de Fluxo de Caixa - Controle Financeiro</p>
        </div>
        <div id="error-message" class="error-message"></div>
        <form id="login-form">
            <div class="form-group">
                <label for="usuario">Usuário</label>
                <input type="text" id="usuario" name="usuario" required placeholder="Digite seu usuário">
            </div>
            <div class="form-group">
                <label for="senha">Senha</label>
                <input type="password" id="senha" name="senha" required placeholder="Digite sua senha">
            </div>
            <button type="submit" class="btn-login">Entrar no Sistema</button>
        </form>
        <div class="footer">
            <p>Use suas credenciais do sistema principal</p>
        </div>
    </div>
    <script>
        document.getElementById('login-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const usuario = document.getElementById('usuario').value;
            const senha = document.getElementById('senha').value;
            const errorDiv = document.getElementById('error-message');
            errorDiv.style.display = 'none';
            try {
                const response = await fetch('/auth', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ usuario, senha })
                });
                const data = await response.json();
                if (data.success) {
                    window.location.href = data.redirect_url;
                } else {
                    errorDiv.textContent = data.message;
                    errorDiv.style.display = 'block';
                }
            } catch (error) {
                errorDiv.textContent = 'Erro de conexão com o servidor';
                errorDiv.style.display = 'block';
            }
        });
    </script>
</body>
</html>
'''

SISTEMA_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projetado INCORPORAÇÃO - Sistema de Fluxo de Caixa</title>
    <style>
        :root {
            --primary-color: #E65100;
            --primary-dark: #BF360C;
            --primary-light: #FF9800;
            --secondary-color: #1976D2;
            --success-color: #4CAF50;
            --warning-color: #FFC107;
            --danger-color: #F44336;
            --light-color: #F5F5F5;
            --dark-color: #212121;
            --gray-color: #757575;
            --border-color: #E0E0E0;
            --shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Roboto', sans-serif;
            background: var(--light-color);
            min-height: 100vh;
            color: var(--dark-color);
        }
        
        /* Header */
        .app-header {
            background: var(--primary-color);
            color: white;
            padding: 1rem 2rem;
            box-shadow: var(--shadow);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header-content h1 {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }
        
        .header-content .subtitle {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        .auth-section {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .admin-info {
            display: flex;
            align-items: center;
            gap: 10px;
            color: white;
            font-weight: 600;
        }
        
        .admin-badge {
            background-color: var(--success-color);
            padding: 4px 8px;
            border-radius: 20px;
            font-size: 11px;
        }
        
        .user-badge {
            background-color: var(--secondary-color);
            padding: 4px 8px;
            border-radius: 20px;
            font-size: 11px;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 13px;
        }
        
        .btn-logout {
            background: var(--danger-color);
            color: white;
        }
        
        .btn-logout:hover {
            background: #d32f2f;
        }
        
        /* Container Principal */
        .container {
            max-width: 95%;
            margin: 1rem auto;
            padding: 0 0.5rem;
        }
        
        /* Painel de Controle */
        .control-panel {
            background: white;
            border-radius: 8px;
            padding: 0.8rem;
            margin-bottom: 1rem;
            box-shadow: var(--shadow);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.8rem;
        }
        
        .controls {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .btn-primary { background: var(--primary-color); color: white; }
        .btn-success { background: var(--success-color); color: white; }
        .btn-warning { background: var(--warning-color); color: var(--dark-color); }
        .btn-danger { background: var(--danger-color); color: white; }
        .btn-secondary { background: var(--secondary-color); color: white; }
        .btn-info { background: #0ea5e9; color: white; }
        
        .btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Status Message */
        .status-message {
            background: #E3F2FD;
            border-left: 4px solid var(--secondary-color);
            padding: 0.6rem;
            margin-bottom: 0.8rem;
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            animation: slideIn 0.3s ease;
            font-size: 0.9rem;
        }
        
        .status-message.success {
            background: #E8F5E9;
            border-left-color: var(--success-color);
        }
        
        .status-message.error {
            background: #FFEBEE;
            border-left-color: var(--danger-color);
        }
        
        .close-btn {
            background: none;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            color: var(--gray-color);
        }
        
        .hidden { display: none !important; }
        
        /* Tabela de Controle */
        .grid-container {
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: var(--shadow);
            margin-bottom: 1rem;
        }
        
        .table-wrapper {
            overflow-x: auto;
            max-height: 70vh;
            overflow-y: auto;
            position: relative;
        }
        
        #fluxoTable {
            width: 100%;
            border-collapse: collapse;
            min-width: 1800px;
            font-size: 12px;
        }
        
        #fluxoTable th {
            background: var(--dark-color);
            color: white;
            padding: 0.6rem;
            text-align: center;
            font-weight: 500;
            position: sticky;
            top: 0;
            z-index: 10;
            min-width: 100px;
            border: 1px solid var(--border-color);
        }
        
        #fluxoTable th.date-column {
            background: var(--primary-color);
            position: sticky;
            left: 0;
            z-index: 20;
            min-width: 80px;
            font-weight: 600;
        }
        
        #fluxoTable th.saldo-column {
            background: #2E7D32;
        }
        
        #fluxoTable th.entrada-column {
            background: #1976D2;
        }
        
        #fluxoTable td {
            padding: 0.4rem;
            text-align: center;
            border: 1px solid var(--border-color);
            font-size: 11px;
        }
        
        #fluxoTable tbody tr:nth-child(even) {
            background-color: #F9F9F9;
        }
        
        #fluxoTable tbody tr:hover {
            background-color: #F0F0F0;
        }
        
        #fluxoTable td:first-child {
            background: var(--light-color);
            font-weight: 500;
            position: sticky;
            left: 0;
            z-index: 5;
            min-width: 80px;
        }
        
        /* Células de entrada */
        .input-cell {
            width: 100%;
            padding: 0.3rem;
            border: 1px solid var(--border-color);
            border-radius: 3px;
            text-align: center;
            font-size: 11px;
            background: white;
            min-height: 28px;
        }
        
        .input-cell:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(230, 81, 0, 0.1);
        }
        
        .input-cell:disabled {
            background: #f8f9fa;
            color: #6c757d;
            cursor: not-allowed;
        }
        
        /* Células de saldo */
        .saldo-cell {
            font-weight: 600;
            padding: 0.4rem;
            border-radius: 3px;
            background: #F1F8E9;
            color: #2E7D32;
            min-height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .saldo-negativo {
            background: #FFEBEE;
            color: #C62828;
        }
        
        .saldo-positivo {
            background: #E8F5E9;
            color: #2E7D32;
        }
        
        /* Status Bar */
        .status-bar {
            background: var(--dark-color);
            color: white;
            padding: 0.8rem;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 0.8rem;
            border-radius: 0 0 8px 8px;
            font-size: 0.8rem;
        }
        
        .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .stat-value {
            font-size: 1rem;
            font-weight: 700;
            color: var(--primary-light);
        }
        
        .stat-label {
            font-size: 0.7rem;
            opacity: 0.8;
        }
        
        /* Modal de Saldo */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        
        .modal-content {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .modal-title {
            font-size: 1.2rem;
            margin-bottom: 1rem;
            color: var(--dark-color);
        }
        
        .modal-input {
            width: 100%;
            padding: 0.6rem;
            margin: 0.8rem 0;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-size: 0.9rem;
        }
        
        .modal-buttons {
            display: flex;
            justify-content: flex-end;
            gap: 0.8rem;
            margin-top: 1rem;
        }
        
        /* Modal Estatísticas */
        #modalEstatisticas .modal-content {
            max-width: 600px;
        }
        
        #estatisticasContent {
            max-height: 400px;
            overflow-y: auto;
        }
        
        /* Loading */
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            display: none;
        }
        
        .loading-spinner {
            width: 30px;
            height: 30px;
            border: 3px solid var(--light-color);
            border-top: 3px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        /* Animações */
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Responsivo */
        @media (max-width: 768px) {
            .control-panel {
                flex-direction: column;
                align-items: stretch;
            }
            
            .controls {
                justify-content: center;
            }
            
            .table-wrapper {
                max-height: 50vh;
            }
            
            .app-header {
                flex-direction: column;
                gap: 0.8rem;
                text-align: center;
            }
            
            .container {
                max-width: 100%;
                padding: 0 0.2rem;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="app-header">
        <div class="header-content">
            <h1>Projetado - INCORPORAÇÃO</h1>
            <p class="subtitle">Sistema de Fluxo de Caixa - Controle Financeiro</p>
        </div>
        <div class="auth-section">
            {% if is_admin %}
            <div class="admin-info">
                <span>Administrador</span>
                <div class="admin-badge">ADM</div>
            </div>
            {% else %}
            <div class="admin-info">
                <span>{{ usuario }}</span>
                <div class="user-badge">{{ setor }}</div>
            </div>
            {% endif %}
            <button class="btn btn-logout" onclick="logout()">
                Sair
            </button>
        </div>
    </header>
    
    <!-- Container Principal -->
    <main class="container">
        <!-- Status Message -->
        <div id="statusMessage" class="status-message hidden">
            <span id="statusText"></span>
            <button onclick="hideStatus()" class="close-btn">&times;</button>
        </div>
        
        <!-- Painel de Controle -->
        <div class="control-panel">
            <div class="controls">
                <button class="btn btn-secondary" onclick="carregarTemplate()">
                    📋 Carregar Template
                </button>
                <button class="btn btn-warning" onclick="validarDados()">
                    ✅ Validar Dados
                </button>
                {% if is_admin %}
                <button class="btn btn-primary" onclick="adicionarSaldo()">
                    💰 Adicionar Saldo
                </button>
                <button class="btn btn-danger" onclick="limparTudo()">
                    🗑️ Limpar Tudo
                </button>
                {% endif %}
            </div>
            <div class="controls">
                <button class="btn btn-success" onclick="exportarExcelCompleto()">
                    📊 Gerar Excel
                </button>
                <button class="btn btn-info" onclick="mostrarEstatisticas()">
                    📈 Estatísticas
                </button>
            </div>
        </div>
        
        <!-- Tabela de Controle -->
        <div class="grid-container">
            <div class="table-wrapper">
                <table id="fluxoTable">
                    <thead id="tableHead"></thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
        </div>
        
        <!-- Status Bar -->
        <div class="status-bar">
            <div class="stat-item">
                <span class="stat-label">Total Empreendimentos</span>
                <span class="stat-value" id="totalEmpreendimentos">8</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Meses</span>
                <span class="stat-value" id="totalMeses">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Total Entradas</span>
                <span class="stat-value" id="totalEntradas">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Saldo Total</span>
                <span class="stat-value" id="saldoTotal">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">API Status</span>
                <span class="stat-value status-online" id="apiStatus">Online</span>
            </div>
        </div>
    </main>
    
    <!-- Modal Adicionar Saldo -->
    <div id="modalSaldo" class="modal">
        <div class="modal-content">
            <h3 class="modal-title">Adicionar Saldo Inicial</h3>
            <div id="saldoInputs"></div>
            <div class="modal-buttons">
                <button class="btn btn-secondary" onclick="fecharModalSaldo()">Cancelar</button>
                <button class="btn btn-success" onclick="salvarSaldosIniciais()">Salvar</button>
            </div>
        </div>
    </div>
    
    <!-- Modal Estatísticas -->
    <div id="modalEstatisticas" class="modal">
        <div class="modal-content">
            <h3 class="modal-title">Estatísticas do Sistema</h3>
            <div id="estatisticasContent"></div>
            <div class="modal-buttons">
                <button class="btn btn-secondary" onclick="fecharModalEstatisticas()">Fechar</button>
            </div>
        </div>
    </div>
    
    <!-- Loading Overlay -->
    <div id="loadingOverlay" class="loading-overlay">
        <div class="loading-spinner"></div>
        <p style="color: white; margin-top: 0.8rem; font-size: 0.9rem;">Processando...</p>
    </div>
    
    <script>
        // Configurações
        let dados = [];
        let meses = [];
        let empreendimentos = {{ empreendimentos|tojson }};
        let isAdmin = {{ 'true' if is_admin else 'false' }};
        let saldosIniciais = {{ saldos_iniciais|tojson }};
        
        // Funções de UI
        function showLoading(show) {
            document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
        }
        
        function showStatus(message, type = 'success') {
            const statusDiv = document.getElementById('statusMessage');
            const statusText = document.getElementById('statusText');
            
            statusText.textContent = message;
            statusDiv.className = `status-message ${type}`;
            statusDiv.classList.remove('hidden');
            
            setTimeout(hideStatus, 5000);
        }
        
        function hideStatus() {
            document.getElementById('statusMessage').classList.add('hidden');
        }
        
        // Carregar dados
        async function carregarDados() {
            showLoading(true);
            try {
                const response = await fetch('/api/dados');
                const result = await response.json();
                
                if (result.success) {
                    dados = result.dados || [];
                    meses = result.meses || [];
                    saldosIniciais = result.saldos_iniciais || {};
                    renderizarTabela();
                    atualizarEstatisticas();
                }
            } catch (error) {
                console.error('Erro ao carregar dados:', error);
                showStatus('Erro ao carregar dados', 'error');
            } finally {
                showLoading(false);
            }
        }
        
        // Renderizar tabela com 2 colunas por empreendimento
        function renderizarTabela() {
            const tableHead = document.getElementById('tableHead');
            const tableBody = document.getElementById('tableBody');
            
            // Limpar tabela
            tableHead.innerHTML = '';
            tableBody.innerHTML = '';
            
            // Criar cabeçalho
            let headerRow = document.createElement('tr');
            
            // Coluna de datas
            let thDate = document.createElement('th');
            thDate.className = 'date-column';
            thDate.textContent = 'Datas';
            headerRow.appendChild(thDate);
            
            // Colunas para cada empreendimento (Saldo + Entrada)
            empreendimentos.forEach(empreendimento => {
                // Coluna do Saldo
                let thSaldo = document.createElement('th');
                thSaldo.className = 'saldo-column';
                thSaldo.textContent = `${empreendimento} - Saldo`;
                thSaldo.title = 'Saldo disponível (somente admin pode editar)';
                headerRow.appendChild(thSaldo);
                
                // Coluna da Entrada
                let thEntrada = document.createElement('th');
                thEntrada.className = 'entrada-column';
                thEntrada.textContent = `${empreendimento} - Entrada`;
                thEntrada.title = 'Valor a ser subtraído do saldo (todos podem editar)';
                headerRow.appendChild(thEntrada);
            });
            
            tableHead.appendChild(headerRow);
            
            // Linhas de meses
            meses.forEach((mes, mesIndex) => {
                let row = document.createElement('tr');
                
                // Coluna da data
                let tdDate = document.createElement('td');
                tdDate.textContent = mes;
                tdDate.style.fontWeight = 'bold';
                row.appendChild(tdDate);
                
                // Colunas para cada empreendimento
                empreendimentos.forEach(empreendimento => {
                    // Encontrar dados deste mês/empreendimento
                    let dadosMes = dados.find(d => d.mes === mes && d.empreendimento === empreendimento);
                    let entradaAtual = dadosMes?.entrada || 0;
                    
                    // Calcular saldo acumulado até este mês
                    let saldoAcumulado = calcularSaldoAcumulado(mes, empreendimento);
                    
                    // Saldo Atual (editável apenas por admin)
                    let tdSaldo = document.createElement('td');
                    if (isAdmin) {
                        let inputSaldo = document.createElement('input');
                        inputSaldo.type = 'number';
                        inputSaldo.className = 'input-cell';
                        inputSaldo.value = saldoAcumulado;
                        inputSaldo.step = '0.01';
                        inputSaldo.min = '0';
                        inputSaldo.dataset.mes = mes;
                        inputSaldo.dataset.empreendimento = empreendimento;
                        inputSaldo.dataset.tipo = 'saldo';
                        inputSaldo.addEventListener('change', function(e) {
                            atualizarSaldo(mes, empreendimento, parseFloat(e.target.value) || 0);
                        });
                        tdSaldo.appendChild(inputSaldo);
                    } else {
                        tdSaldo.className = `saldo-cell ${saldoAcumulado < 0 ? 'saldo-negativo' : 'saldo-positivo'}`;
                        tdSaldo.textContent = formatarNumero(saldoAcumulado);
                    }
                    row.appendChild(tdSaldo);
                    
                    // Entrada (input) - TODOS podem editar
                    let tdEntrada = document.createElement('td');
                    let inputEntrada = document.createElement('input');
                    inputEntrada.type = 'number';
                    inputEntrada.className = 'input-cell';
                    inputEntrada.value = entradaAtual;
                    inputEntrada.step = '0.01';
                    inputEntrada.min = '0';
                    inputEntrada.placeholder = '0.00';
                    inputEntrada.dataset.mes = mes;
                    inputEntrada.dataset.empreendimento = empreendimento;
                    inputEntrada.dataset.tipo = 'entrada';
                    
                    // Evento para atualizar entrada
                    inputEntrada.addEventListener('change', function(e) {
                        atualizarEntrada(mes, empreendimento, parseFloat(e.target.value) || 0);
                    });
                    
                    tdEntrada.appendChild(inputEntrada);
                    row.appendChild(tdEntrada);
                });
                
                tableBody.appendChild(row);
            });
        }
        
        // Calcular saldo acumulado até um mês específico
        function calcularSaldoAcumulado(mes, empreendimento) {
            // Saldo inicial
            let saldo = saldosIniciais[empreendimento] || 0;
            
            // Encontrar índice do mês atual
            const mesIndex = meses.indexOf(mes);
            if (mesIndex === -1) return saldo;
            
            // Subtrair todas as entradas até este mês
            for (let i = 0; i <= mesIndex; i++) {
                const mesAtual = meses[i];
                const dadosMes = dados.find(d => d.mes === mesAtual && d.empreendimento === empreendimento);
                if (dadosMes && dadosMes.entrada) {
                    saldo -= dadosMes.entrada;
                }
            }
            
            return saldo;
        }
        
        // Atualizar entrada (TODOS podem fazer)
        async function atualizarEntrada(mes, empreendimento, valor) {
            if (valor < 0) {
                showStatus('Valor de entrada não pode ser negativo', 'error');
                return;
            }
            
            showLoading(true);
            
            try {
                const response = await fetch('/api/atualizar-entrada', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        mes: mes,
                        empreendimento: empreendimento,
                        entrada: valor
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Atualizar dados locais
                    let index = dados.findIndex(d => d.mes === mes && d.empreendimento === empreendimento);
                    
                    if (index >= 0) {
                        dados[index].entrada = valor;
                    } else {
                        dados.push({
                            mes: mes,
                            empreendimento: empreendimento,
                            entrada: valor
                        });
                    }
                    
                    // Recalcular e renderizar tabela
                    renderizarTabela();
                    atualizarEstatisticas();
                    showStatus('Entrada atualizada com sucesso');
                } else {
                    showStatus('Erro ao atualizar: ' + result.error, 'error');
                }
            } catch (error) {
                console.error('Erro ao atualizar entrada:', error);
                showStatus('Erro ao atualizar entrada', 'error');
            } finally {
                showLoading(false);
            }
        }
        
        // Atualizar saldo (APENAS ADMIN)
        async function atualizarSaldo(mes, empreendimento, valor) {
            if (!isAdmin) {
                showStatus('Apenas administradores podem atualizar saldos', 'error');
                return;
            }
            
            showLoading(true);
            
            try {
                const response = await fetch('/api/atualizar-saldo', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        empreendimento: empreendimento,
                        saldo: valor
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    saldosIniciais[empreendimento] = valor;
                    renderizarTabela();
                    atualizarEstatisticas();
                    showStatus('Saldo inicial atualizado');
                }
            } catch (error) {
                console.error('Erro ao atualizar saldo:', error);
                showStatus('Erro ao atualizar saldo', 'error');
            } finally {
                showLoading(false);
            }
        }
        
        // Carregar template
        async function carregarTemplate() {
            showLoading(true);
            
            try {
                const response = await fetch('/api/carregar-template', { method: 'POST' });
                const result = await response.json();
                
                if (result.success) {
                    meses = result.meses;
                    saldosIniciais = result.saldos_iniciais || {};
                    dados = [];
                    renderizarTabela();
                    atualizarEstatisticas();
                    showStatus('Template carregado com sucesso');
                }
            } catch (error) {
                console.error('Erro ao carregar template:', error);
                showStatus('Erro ao carregar template', 'error');
            } finally {
                showLoading(false);
            }
        }
        
        // Validar dados
        async function validarDados() {
            showLoading(true);
            
            try {
                const response = await fetch('/api/validar-dados', { method: 'POST' });
                const result = await response.json();
                
                if (result.success) {
                    if (result.erros && result.erros.length > 0) {
                        showStatus('Dados validados com ' + result.erros.length + ' erros', 'error');
                        console.warn('Erros encontrados:', result.erros);
                    } else {
                        showStatus('Todos os dados estão válidos');
                    }
                }
            } catch (error) {
                console.error('Erro ao validar dados:', error);
                showStatus('Erro ao validar dados', 'error');
            } finally {
                showLoading(false);
            }
        }
        
        // Adicionar saldo (modal)
        function adicionarSaldo() {
            if (!isAdmin) {
                showStatus('Apenas administradores podem adicionar saldo', 'error');
                return;
            }
            
            const modal = document.getElementById('modalSaldo');
            const inputsDiv = document.getElementById('saldoInputs');
            inputsDiv.innerHTML = '';
            
            empreendimentos.forEach(empreendimento => {
                const div = document.createElement('div');
                div.style.marginBottom = '8px';
                div.style.display = 'flex';
                div.style.alignItems = 'center';
                
                const label = document.createElement('label');
                label.textContent = `${empreendimento}: `;
                label.style.display = 'inline-block';
                label.style.width = '120px';
                label.style.fontSize = '0.9rem';
                
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'modal-input';
                input.value = saldosIniciais[empreendimento] || 0;
                input.step = '0.01';
                input.min = '0';
                input.dataset.empreendimento = empreendimento;
                input.style.flex = '1';
                
                div.appendChild(label);
                div.appendChild(input);
                inputsDiv.appendChild(div);
            });
            
            modal.style.display = 'flex';
        }
        
        function fecharModalSaldo() {
            document.getElementById('modalSaldo').style.display = 'none';
        }
        
        async function salvarSaldosIniciais() {
            showLoading(true);
            
            try {
                const inputs = document.querySelectorAll('#saldoInputs input');
                const novosSaldos = {};
                
                inputs.forEach(input => {
                    const empreendimento = input.dataset.empreendimento;
                    novosSaldos[empreendimento] = parseFloat(input.value) || 0;
                });
                
                const response = await fetch('/api/atualizar-saldos', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ saldos: novosSaldos })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    saldosIniciais = result.saldos;
                    fecharModalSaldo();
                    renderizarTabela();
                    atualizarEstatisticas();
                    showStatus('Saldos iniciais atualizados');
                }
            } catch (error) {
                console.error('Erro ao salvar saldos:', error);
                showStatus('Erro ao salvar saldos', 'error');
            } finally {
                showLoading(false);
            }
        }
        
        // Limpar tudo (apenas admin)
        async function limparTudo() {
            if (!isAdmin) {
                showStatus('Apenas administradores podem limpar dados', 'error');
                return;
            }
            
            if (!confirm('Tem certeza que deseja limpar todos os dados? Esta ação não pode ser desfeita.')) {
                return;
            }
            
            showLoading(true);
            
            try {
                const response = await fetch('/api/limpar-tudo', { method: 'POST' });
                const result = await response.json();
                
                if (result.success) {
                    dados = [];
                    saldosIniciais = result.saldos_iniciais || {};
                    renderizarTabela();
                    atualizarEstatisticas();
                    showStatus('Todos os dados foram limpos');
                }
            } catch (error) {
                console.error('Erro ao limpar dados:', error);
                showStatus('Erro ao limpar dados', 'error');
            } finally {
                showLoading(false);
            }
        }
        
        // Exportar Excel com estrutura completa
        async function exportarExcelCompleto() {
            showLoading(true);
            
            try {
                const response = await fetch('/api/exportar-excel-completo');
                const blob = await response.blob();
                
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `Fluxo_Caixa_Projetado_${new Date().toISOString().split('T')[0]}.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                
                showStatus('Excel exportado com estrutura completa!');
            } catch (error) {
                console.error('Erro ao exportar:', error);
                showStatus('Erro ao exportar Excel', 'error');
            } finally {
                showLoading(false);
            }
        }
        
        // Mostrar estatísticas
        async function mostrarEstatisticas() {
            const modal = document.getElementById('modalEstatisticas');
            const contentDiv = document.getElementById('estatisticasContent');
            
            // Calcular estatísticas
            let totalEntradas = 0;
            let saldoTotal = 0;
            let empreendimentosStats = {};
            
            empreendimentos.forEach(empreendimento => {
                const saldoInicial = saldosIniciais[empreendimento] || 0;
                let entradasEmpreendimento = 0;
                
                dados.filter(d => d.empreendimento === empreendimento).forEach(d => {
                    entradasEmpreendimento += d.entrada || 0;
                });
                
                totalEntradas += entradasEmpreendimento;
                const saldoFinal = saldoInicial - entradasEmpreendimento;
                saldoTotal += saldoFinal;
                
                empreendimentosStats[empreendimento] = {
                    saldo_inicial: saldoInicial,
                    entradas: entradasEmpreendimento,
                    saldo_final: saldoFinal
                };
            });
            
            // Construir conteúdo
            let html = `
                <div style="margin-bottom: 1rem;">
                    <h4 style="color: var(--primary-color); margin-bottom: 0.5rem;">Resumo Geral</h4>
                    <p><strong>Total de Empreendimentos:</strong> ${empreendimentos.length}</p>
                    <p><strong>Total de Meses:</strong> ${meses.length}</p>
                    <p><strong>Total de Entradas:</strong> ${formatarNumero(totalEntradas)}</p>
                    <p><strong>Saldo Total:</strong> <span style="color: ${saldoTotal >= 0 ? '#2E7D32' : '#C62828'}">${formatarNumero(saldoTotal)}</span></p>
                </div>
                
                <div style="margin-bottom: 1rem;">
                    <h4 style="color: var(--primary-color); margin-bottom: 0.5rem;">Por Empreendimento</h4>
            `;
            
            empreendimentos.forEach(empreendimento => {
                const stats = empreendimentosStats[empreendimento];
                html += `
                    <div style="background: #f5f5f5; padding: 0.5rem; margin-bottom: 0.5rem; border-radius: 4px;">
                        <strong>${empreendimento}</strong>
                        <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                            <span>Saldo Inicial: ${formatarNumero(stats.saldo_inicial)}</span>
                            <span>Entradas: ${formatarNumero(stats.entradas)}</span>
                            <span style="color: ${stats.saldo_final >= 0 ? '#2E7D32' : '#C62828'}">
                                Saldo Final: ${formatarNumero(stats.saldo_final)}
                            </span>
                        </div>
                    </div>
                `;
            });
            
            html += `</div>`;
            
            contentDiv.innerHTML = html;
            modal.style.display = 'flex';
        }
        
        function fecharModalEstatisticas() {
            document.getElementById('modalEstatisticas').style.display = 'none';
        }
        
        // Atualizar estatísticas
        function atualizarEstatisticas() {
            // Totais
            let totalEntradas = 0;
            let saldoTotal = 0;
            
            dados.forEach(d => {
                totalEntradas += d.entrada || 0;
            });
            
            empreendimentos.forEach(empreendimento => {
                const saldoInicial = saldosIniciais[empreendimento] || 0;
                let entradasEmpreendimento = 0;
                
                dados.filter(d => d.empreendimento === empreendimento).forEach(d => {
                    entradasEmpreendimento += d.entrada || 0;
                });
                
                saldoTotal += (saldoInicial - entradasEmpreendimento);
            });
            
            document.getElementById('totalEmpreendimentos').textContent = empreendimentos.length;
            document.getElementById('totalMeses').textContent = meses.length;
            document.getElementById('totalEntradas').textContent = formatarNumero(totalEntradas);
            document.getElementById('saldoTotal').textContent = formatarNumero(saldoTotal);
        }
        
        // Utilitários
        function formatarNumero(valor) {
            return new Intl.NumberFormat('pt-BR', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(valor);
        }
        
        function logout() {
            window.location.href = '/logout';
        }
        
        // Inicialização
        document.addEventListener('DOMContentLoaded', () => {
            carregarDados();
            
            // Atualizar estatísticas periodicamente
            setInterval(atualizarEstatisticas, 30000);
        });
    </script>
</body>
</html>
'''