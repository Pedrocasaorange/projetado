from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List

@dataclass
class CashFlowData:
    """Data model for cash flow entries"""
    date: str
    projects: Dict[str, float]
    
    def to_dict(self):
        return asdict(self)

class CashFlowModel:
    """Business logic and data management"""
    
    PROJECTS = [
        "ALLEGRO", "PIAZZA", "CASA PARQUE", "CASA BOA VIAGEM",
        "CASA MAYOR", "CASA ORIZON", "CASA DO POÇO", "CASA MAR"
    ]
    
    @staticmethod
    def generate_dates() -> List[str]:
        """Generate dates from nov/25 to jan/27"""
        dates = []
        start_date = datetime(2025, 11, 1)
        end_date = datetime(2030, 12, 30)
        
        current_date = start_date
        while current_date < end_date:
            month_abbr = current_date.strftime("%b").lower()[:3]
            year_short = current_date.strftime("%y")
            dates.append(f"{month_abbr}/{year_short}")
            current_date += timedelta(days=32)
            current_date = current_date.replace(day=1)
        
        return dates
    
    @staticmethod
    def create_template() -> List[Dict]:
        """Create empty template data structure"""
        dates = CashFlowModel.generate_dates()
        template = []
        
        for date in dates:
            projects = {projeto: 0.0 for projeto in CashFlowModel.PROJECTS}
            template.append({
                "date": date,
                "projects": projects
            })
        
        return template
    
    @staticmethod
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
    
    @staticmethod
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