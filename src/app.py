from flask import Flask, jsonify, request, send_file, make_response, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO
import os

# Create Flask app
app = Flask(__name__)
CORS(app)

# Projetos definidos
PROJECTS = [
    "ALLEGRO", "PIAZZA", "CASA PARQUE", "CASA BOA VIAGEM",
    "CASA MAYOR", "CASA ORIZON", "CASA DO POÇO", "CASA MAR"
]

def generate_dates():
    """Generate dates from nov/25 to jan/27"""
    dates = []
    start_date = datetime(2025, 11, 1)
    end_date = datetime(2027, 2, 1)
    
    current_date = start_date
    while current_date < end_date:
        month_abbr = current_date.strftime("%b").lower()[:3]
        year_short = current_date.strftime("%y")
        dates.append(f"{month_abbr}/{year_short}")
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)
    
    return dates

def parse_brazilian_number(value: str) -> float:
    """Parse Brazilian number format (1.000,00) to float"""
    if not value or value.strip() == '':
        return 0.0
    
    try:
        value = str(value).strip()
        value = value.replace('.', '')
        value = value.replace(',', '.')
        
        if value.count('.') > 1:
            parts = value.split('.')
            value = ''.join(parts[:-1]) + '.' + parts[-1]
        
        return float(value)
    except (ValueError, AttributeError):
        raise ValueError(f"Valor inválido: {value}")

def format_brazilian_number(value: float) -> str:
    """Format float to Brazilian number format"""
    try:
        if value == 0:
            return "0,00"
        
        # Format with 2 decimal places and thousand separators
        formatted = f"{value:,.2f}"
        parts = formatted.split('.')
        integer_part = parts[0].replace(',', '.')
        return f"{integer_part},{parts[1]}"
    except:
        return "0,00"

def create_template() -> list:
    """Create empty template data structure"""
    dates = generate_dates()
    template = []
    
    for date in dates:
        projects = {projeto: "0,00" for projeto in PROJECTS}
        template.append({
            "date": date,
            "projects": projects
        })
    
    return template

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'CashFlow API',
        'timestamp': datetime.now().isoformat()
    })

# Get empty template
@app.route('/api/template', methods=['GET'])
def get_template():
    """Get empty cash flow template"""
    try:
        template_data = create_template()
        
        return jsonify({
            'success': True,
            'data': {
                'template': template_data,
                'projects': PROJECTS
            },
            'message': 'Template carregado com sucesso'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao carregar template: {str(e)}'
        }), 500

# Validate data
@app.route('/api/validate', methods=['POST'])
def validate_data():
    """Validate cash flow data"""
    try:
        data = request.get_json()
        
        if not data or 'rows' not in data:
            return jsonify({
                'success': False,
                'message': 'Dados inválidos'
            }), 400
        
        validated_data = []
        errors = []
        
        for row in data['rows']:
            try:
                date = row.get('date', '')
                projects = row.get('projects', {})
                
                validated_projects = {}
                for projeto in PROJECTS:
                    value = projects.get(projeto, '0,00')
                    if isinstance(value, str):
                        validated_projects[projeto] = parse_brazilian_number(value)
                    else:
                        validated_projects[projeto] = float(value)
                
                validated_data.append({
                    'date': date,
                    'projects': validated_projects
                })
                
            except Exception as e:
                errors.append(f"Erro na linha {row.get('date', 'desconhecida')}: {str(e)}")
        
        if len(errors) == 0:
            return jsonify({
                'success': True,
                'data': validated_data,
                'message': 'Dados validados com sucesso'
            })
        else:
            return jsonify({
                'success': False,
                'errors': errors,
                'message': 'Erros encontrados na validação'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro na validação: {str(e)}'
        }), 500

# Export to Excel
@app.route('/api/export', methods=['POST'])
def export_to_excel():
    """Export cash flow data to Excel"""
    try:
        data = request.get_json()
        
        if not data or 'rows' not in data:
            return jsonify({
                'success': False,
                'message': 'Dados inválidos'
            }), 400
        
        # Validate data first
        validated_data = []
        errors = []
        
        for row in data['rows']:
            try:
                date = row.get('date', '')
                projects = row.get('projects', {})
                
                validated_projects = {}
                for projeto in PROJECTS:
                    value = projects.get(projeto, '0,00')
                    if isinstance(value, str):
                        validated_projects[projeto] = parse_brazilian_number(value)
                    else:
                        validated_projects[projeto] = float(value)
                
                validated_data.append({
                    'date': date,
                    'projects': validated_projects
                })
                
            except Exception as e:
                errors.append(f"Erro na linha {row.get('date', 'desconhecida')}: {str(e)}")
        
        if len(errors) > 0:
            return jsonify({
                'success': False,
                'errors': errors,
                'message': 'Corrija os erros antes de exportar'
            }), 400
        
        # Create DataFrame
        df_data = []
        for row in validated_data:
            row_data = {'Datas': row['date']}
            row_data.update(row['projects'])
            df_data.append(row_data)
        
        df = pd.DataFrame(df_data)
        df.set_index('Datas', inplace=True)
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Fluxo de Caixa')
            
            # Format the worksheet
            worksheet = writer.sheets['Fluxo de Caixa']
            
            # Set column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 30)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        
        # Create response
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'fluxo_caixa_{timestamp}.xlsx'
        
        response = make_response(send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        ))
        
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao gerar Excel: {str(e)}'
        }), 500

# Serve frontend files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend files"""
    frontend_path = os.path.join('..', 'front')
    
    if path != "" and os.path.exists(os.path.join(frontend_path, path)):
        return send_from_directory(frontend_path, path)
    else:
        return send_from_directory(frontend_path, 'index.html')

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Sistema de Fluxo de Caixa - INCORPORAÇÃO")
    print("=" * 50)
    print("📊 API disponível em: http://localhost:5000/api")
    print("🌐 Frontend disponível em: http://localhost:5000")
    print("🔧 Health Check: http://localhost:5000/health")
    print("=" * 50)
    print("📁 Projetos disponíveis:")
    for i, projeto in enumerate(PROJECTS, 1):
        print(f"   {i}. {projeto}")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)