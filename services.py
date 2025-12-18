import pandas as pd
from io import BytesIO
from datetime import datetime
from model import CashFlowModel

class CashFlowService:
    """Service layer for cash flow operations"""
    
    @staticmethod
    def validate_data(data: list) -> dict:
        """Validate incoming cash flow data"""
        validated_data = []
        errors = []
        
        for row in data:
            try:
                date = row.get('date', '')
                projects = row.get('projects', {})
                
                validated_projects = {}
                for projeto in CashFlowModel.PROJECTS:
                    value = projects.get(projeto, '0,00')
                    if isinstance(value, str):
                        validated_projects[projeto] = CashFlowModel.parse_brazilian_number(value)
                    else:
                        validated_projects[projeto] = float(value)
                
                validated_data.append({
                    'date': date,
                    'projects': validated_projects
                })
                
            except Exception as e:
                errors.append(f"Erro na linha {row.get('date', 'desconhecida')}: {str(e)}")
        
        return {
            'data': validated_data,
            'errors': errors,
            'valid': len(errors) == 0
        }
    
    @staticmethod
    def generate_excel(data: list) -> BytesIO:
        """Generate Excel file from cash flow data"""
        df_data = []
        for row in data:
            row_data = {'Datas': row['date']}
            row_data.update(row['projects'])
            df_data.append(row_data)
        
        df = pd.DataFrame(df_data)
        df.set_index('Datas', inplace=True)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Fluxo de Caixa')
            
            worksheet = writer.sheets['Fluxo de Caixa']
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
        return output
    
    @staticmethod
    def get_template() -> dict:
        """Get empty template with formatted values"""
        template = CashFlowModel.create_template()
        
        formatted_template = []
        for item in template:
            formatted_projects = {}
            for projeto, value in item['projects'].items():
                formatted_projects[projeto] = CashFlowModel.format_brazilian_number(value)
            
            formatted_template.append({
                'date': item['date'],
                'projects': formatted_projects
            })
        
        return {
            'template': formatted_template,
            'projects': CashFlowModel.PROJECTS
        }