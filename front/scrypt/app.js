// Configuration
const API_BASE_URL = '/api';  // Corrigido para usar caminho relativo
let cashflowData = [];
let projects = [];

// DOM Elements
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
const totalRowsSpan = document.getElementById('totalRows');
const totalProjectsSpan = document.getElementById('totalProjects');
const lastUpdateSpan = document.getElementById('lastUpdate');
const apiStatusSpan = document.getElementById('apiStatus');

// API Service
const apiService = {
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    },

    async getTemplate() {
        return this.request('/template');
    },

    async validateData(data) {
        return this.request('/validate', {
            method: 'POST',
            body: JSON.stringify({ rows: data })
        });
    },

    async exportToExcel(data) {
        const response = await fetch(`${API_BASE_URL}/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rows: data })
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || 'Erro ao exportar');
        }

        // Create blob and download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        // Try to get filename from headers
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'fluxo_caixa.xlsx';
        if (contentDisposition) {
            const match = contentDisposition.match(/filename="(.+)"/);
            if (match) filename = match[1];
        }
        
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
};

// UI Utilities
const uiUtils = {
    showLoading() {
        loadingOverlay.classList.remove('hidden');
    },

    hideLoading() {
        loadingOverlay.classList.add('hidden');
    },

    showStatus(message, type = 'info') {
        statusText.textContent = message;
        statusMessage.className = `status-message ${type}`;
        statusMessage.classList.remove('hidden');
        
        // Auto-hide after 5 seconds for success messages
        if (type === 'success') {
            setTimeout(() => {
                this.hideStatus();
            }, 5000);
        }
    },

    hideStatus() {
        statusMessage.classList.add('hidden');
    },

    updateStats() {
        totalRowsSpan.textContent = `${cashflowData.length} meses`;
        totalProjectsSpan.textContent = `${projects.length} projetos`;
        lastUpdateSpan.textContent = new Date().toLocaleTimeString('pt-BR');
    },

    checkApiStatus() {
        fetch('/health')
            .then(response => {
                if (response.ok) {
                    apiStatusSpan.textContent = 'Online';
                    apiStatusSpan.className = 'status-online';
                    return true;
                } else {
                    throw new Error('API offline');
                }
            })
            .catch(() => {
                apiStatusSpan.textContent = 'Offline';
                apiStatusSpan.className = 'status-offline';
                return false;
            });
    },

    formatBrazilianNumber(value) {
        if (value === null || value === undefined || value === '') return '0,00';
        
        const num = parseFloat(value);
        if (isNaN(num)) return '0,00';
        
        return num.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    },

    parseBrazilianNumber(value) {
        if (!value) return '0';
        return value.toString().replace(/\./g, '').replace(',', '.');
    }
};

// Data Grid Management
const dataGrid = {
    initTable() {
        // Clear existing content
        tableHead.innerHTML = '<th class="fixed-header date-column">Datas</th>';
        tableBody.innerHTML = '';

        // Create project headers
        projects.forEach(project => {
            const th = document.createElement('th');
            th.textContent = project;
            th.title = project;
            th.style.minWidth = '120px';
            tableHead.appendChild(th);
        });

        // Create rows
        cashflowData.forEach((row, rowIndex) => {
            const tr = document.createElement('tr');
            
            // Date cell
            const dateTd = document.createElement('td');
            dateTd.textContent = row.date;
            dateTd.style.fontWeight = '500';
            tr.appendChild(dateTd);

            // Project cells
            projects.forEach(project => {
                const td = document.createElement('td');
                const input = document.createElement('input');
                
                input.type = 'text';
                input.className = 'input-cell';
                input.value = row.projects[project] || '0,00';
                input.dataset.date = row.date;
                input.dataset.project = project;
                
                // Add input events
                input.addEventListener('focus', (e) => this.handleInputFocus(e));
                input.addEventListener('blur', (e) => this.handleInputBlur(e));
                input.addEventListener('keypress', (e) => this.handleKeyPress(e));
                
                td.appendChild(input);
                tr.appendChild(td);
            });

            tableBody.appendChild(tr);
        });

        uiUtils.updateStats();
    },

    handleInputFocus(event) {
        event.target.select();
    },

    handleInputBlur(event) {
        const input = event.target;
        const value = input.value.trim();
        
        // Format the number on blur
        if (value) {
            const numericValue = uiUtils.parseBrazilianNumber(value);
            const floatValue = parseFloat(numericValue);
            
            if (!isNaN(floatValue)) {
                input.value = uiUtils.formatBrazilianNumber(floatValue);
                input.classList.remove('invalid');
                
                // Update data model
                this.updateDataModel(input.dataset.date, input.dataset.project, floatValue);
            } else {
                input.classList.add('invalid');
                uiUtils.showStatus('Formato inválido. Use números no formato brasileiro (ex: 1.000,00)', 'error');
            }
        }
    },

    handleKeyPress(event) {
        if (event.key === 'Enter') {
            event.target.blur();
        }
        
        // Allow only numbers, comma, dot, and control keys
        const allowedKeys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', 
                           'Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab', 'Enter'];
        
        if (!allowedKeys.includes(event.key) && !event.ctrlKey && !event.metaKey) {
            event.preventDefault();
        }
    },

    updateDataModel(date, project, value) {
        const row = cashflowData.find(r => r.date === date);
        if (row) {
            row.projects[project] = value;
        }
    },

    getCurrentData() {
        // Collect data from all inputs
        const inputs = document.querySelectorAll('.input-cell');
        inputs.forEach(input => {
            const value = uiUtils.parseBrazilianNumber(input.value);
            const floatValue = parseFloat(value);
            
            if (!isNaN(floatValue)) {
                this.updateDataModel(input.dataset.date, input.dataset.project, floatValue);
            }
        });
        
        return cashflowData;
    },

    clearAll() {
        cashflowData.forEach(row => {
            projects.forEach(project => {
                row.projects[project] = 0;
            });
        });
        
        this.initTable();
        uiUtils.showStatus('Todos os dados foram limpos', 'success');
    }
};

// Event Handlers
async function handleLoadTemplate() {
    try {
        uiUtils.showLoading();
        const response = await apiService.getTemplate();
        
        if (response.success) {
            cashflowData = response.data.template;
            projects = response.data.projects;
            
            // Parse formatted strings to numbers
            cashflowData.forEach(row => {
                Object.keys(row.projects).forEach(project => {
                    const value = row.projects[project];
                    row.projects[project] = parseFloat(uiUtils.parseBrazilianNumber(value));
                });
            });
            
            dataGrid.initTable();
            uiUtils.showStatus('Template carregado com sucesso', 'success');
        } else {
            throw new Error(response.message);
        }
    } catch (error) {
        console.error('Error loading template:', error);
        uiUtils.showStatus(`Erro ao carregar template: ${error.message}`, 'error');
    } finally {
        uiUtils.hideLoading();
    }
}

async function handleValidateData() {
    try {
        uiUtils.showLoading();
        const currentData = dataGrid.getCurrentData();
        
        // Format data for API
        const formattedData = currentData.map(row => ({
            date: row.date,
            projects: Object.fromEntries(
                Object.entries(row.projects).map(([key, value]) => [
                    key, uiUtils.formatBrazilianNumber(value)
                ])
            )
        }));
        
        const response = await apiService.validateData(formattedData);
        
        if (response.success) {
            uiUtils.showStatus('Dados validados com sucesso!', 'success');
        } else {
            const errorList = response.errors.join('\n• ');
            uiUtils.showStatus(`Erros encontrados:\n• ${errorList}`, 'error');
        }
    } catch (error) {
        console.error('Error validating data:', error);
        uiUtils.showStatus(`Erro na validação: ${error.message}`, 'error');
    } finally {
        uiUtils.hideLoading();
    }
}

async function handleExportExcel() {
    try {
        uiUtils.showLoading();
        const currentData = dataGrid.getCurrentData();
        
        // Format data for API
        const formattedData = currentData.map(row => ({
            date: row.date,
            projects: Object.fromEntries(
                Object.entries(row.projects).map(([key, value]) => [
                    key, uiUtils.formatBrazilianNumber(value)
                ])
            )
        }));
        
        await apiService.exportToExcel(formattedData);
        uiUtils.showStatus('Arquivo Excel gerado com sucesso!', 'success');
    } catch (error) {
        console.error('Error exporting to Excel:', error);
        uiUtils.showStatus(`Erro ao gerar Excel: ${error.message}`, 'error');
    } finally {
        uiUtils.hideLoading();
    }
}

function handleClearAll() {
    if (confirm('Tem certeza que deseja limpar todos os dados? Esta ação não pode ser desfeita.')) {
        dataGrid.clearAll();
    }
}

// Initialize Application
function initApp() {
    console.log('🚀 Inicializando aplicação de Fluxo de Caixa...');
    
    // Check API status on startup
    const apiOnline = uiUtils.checkApiStatus();
    
    if (!apiOnline) {
        uiUtils.showStatus('API offline. Verifique se o servidor está rodando.', 'error');
    }
    
    // Bind event handlers
    loadTemplateBtn.addEventListener('click', handleLoadTemplate);
    validateDataBtn.addEventListener('click', handleValidateData);
    exportExcelBtn.addEventListener('click', handleExportExcel);
    clearAllBtn.addEventListener('click', handleClearAll);
    closeStatusBtn.addEventListener('click', () => uiUtils.hideStatus());
    
    // Load template automatically
    setTimeout(handleLoadTemplate, 500);
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (event) => {
        // Ctrl + L to load template
        if (event.ctrlKey && event.key === 'l') {
            event.preventDefault();
            handleLoadTemplate();
        }
        
        // Ctrl + S to save/export
        if (event.ctrlKey && event.key === 's') {
            event.preventDefault();
            handleExportExcel();
        }
        
        // Ctrl + V to validate
        if (event.ctrlKey && event.key === 'v') {
            event.preventDefault();
            handleValidateData();
        }
    });
    
    console.log('✅ Aplicação inicializada com sucesso!');
}

// Start the application when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);