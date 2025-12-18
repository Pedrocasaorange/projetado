/**
 * APP.JS - SISTEMA DE FLUXO DE CAIXA (CORRIGIDO)
 * Versão sincronizada com FastAPI (run.py) na porta 8000
 */

// 1. Configuração de Conexão (Usa caminhos relativos para evitar erros 404)
const API_BASE_URL = ''; 
let cashflowData = [];
let projects = [];

// 2. Elementos do DOM
const tableBody = document.querySelector('#cashflowTable tbody');
const tableHead = document.querySelector('#cashflowTable thead tr');
const loadTemplateBtn = document.getElementById('loadTemplate');
const validateDataBtn = document.getElementById('validateData');
const exportExcelBtn = document.getElementById('exportExcel');
const clearAllBtn = document.getElementById('clearAll');
const statusMessage = document.getElementById('statusMessage');
const statusText = document.getElementById('statusText');
const closeStatusBtn = document.getElementById('closeStatus');
const loadingOverlay = document.getElementById('loadingOverlay');
const apiStatusSpan = document.getElementById('apiStatus');

// 3. Serviço de API (Centraliza as chamadas ao run.py)
const apiService = {
    async request(endpoint, options = {}) {
        // Garante que o endpoint comece com /
        const url = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
        
        const defaultOptions = {
            headers: { 'Content-Type': 'application/json' },
        };

        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Falha na requisição [${url}]:`, error);
            throw error;
        }
    },

    // Checa se a API está viva (Resolve o Status Online/Offline)
    async checkApiStatus() {
        try {
            await this.request('/api/health');
            apiStatusSpan.textContent = 'Online';
            apiStatusSpan.className = 'status-online';
            return true;
        } catch (error) {
            apiStatusSpan.textContent = 'Offline';
            apiStatusSpan.className = 'status-offline';
            return false;
        }
    }
};

// 4. Utilitários de UI
const uiUtils = {
    showLoading(show) {
        loadingOverlay.classList.toggle('hidden', !show);
    },
    showStatus(message, type = 'success') {
        statusText.textContent = message;
        statusMessage.className = `status-message ${type}`;
        statusMessage.classList.remove('hidden');
        setTimeout(() => this.hideStatus(), 5000);
    },
    hideStatus() {
        statusMessage.classList.add('hidden');
    }
};

// 5. Handlers (Lógica de Negócio)

// Carrega o Template Inicial (Resolve o erro "Error loading template")
async function handleLoadTemplate() {
    uiUtils.showLoading(true);
    try {
        const response = await apiService.request('/api/template');
        if (response.status === 'sucesso') {
            cashflowData = response.data.template;
            projects = response.data.projects;
            renderTable();
            uiUtils.showStatus('Template carregado com sucesso!');
        }
    } catch (error) {
        uiUtils.showStatus('Erro ao carregar template. Verifique o servidor.', 'error');
    } finally {
        uiUtils.showLoading(false);
    }
}

// Renderiza a tabela na tela
function renderTable() {
    // Cabeçalho
    tableHead.innerHTML = '<th class="fixed-header date-column">Datas</th>';
    projects.forEach(proj => {
        const th = document.createElement('th');
        th.textContent = proj;
        tableHead.appendChild(th);
    });

    // Corpo
    tableBody.innerHTML = '';
    cashflowData.forEach((row, rowIndex) => {
        const tr = document.createElement('tr');
        
        // Coluna de Data
        const tdDate = document.createElement('td');
        tdDate.className = 'date-cell';
        tdDate.textContent = row.date;
        tr.appendChild(tdDate);

        // Colunas de Projetos
        projects.forEach(proj => {
            const td = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'cell-input';
            input.value = row.projects[proj] || '0,00';
            
            input.addEventListener('change', (e) => {
                cashflowData[rowIndex].projects[proj] = e.target.value;
            });
            
            td.appendChild(input);
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}

// Valida os dados (Botão Laranja)
async function handleValidateData() {
    uiUtils.showLoading(true);
    try {
        const response = await apiService.request('/api/validate', {
            method: 'POST',
            body: JSON.stringify({ data: cashflowData })
        });
        if (response.status === 'sucesso') {
            uiUtils.showStatus('Dados validados com sucesso!');
        }
    } catch (error) {
        uiUtils.showStatus('Erro na validação.', 'error');
    } finally {
        uiUtils.showLoading(false);
    }
}

// Exporta para Excel (Botão Verde)
async function handleExportExcel() {
    uiUtils.showLoading(true);
    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: cashflowData })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `fluxo_caixa_projetado_${new Date().getTime()}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            uiUtils.showStatus('Arquivo exportado com sucesso!');
        }
    } catch (error) {
        uiUtils.showStatus('Erro ao exportar arquivo.', 'error');
    } finally {
        uiUtils.showLoading(false);
    }
}

// 6. Inicialização
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Inicializando aplicação...');
    
    // Liga os botões
    loadTemplateBtn.addEventListener('click', handleLoadTemplate);
    validateDataBtn.addEventListener('click', handleValidateData);
    exportExcelBtn.addEventListener('click', handleExportExcel);
    clearAllBtn.addEventListener('click', () => location.reload());
    closeStatusBtn.addEventListener('click', () => uiUtils.hideStatus());

    // Checa API e carrega template inicial
    apiService.checkApiStatus();
    setTimeout(handleLoadTemplate, 500);
});