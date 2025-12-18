import re

def validate_brazilian_number(value: str) -> bool:
    """Validate if string is in Brazilian number format"""
    pattern = r'^[0-9]{1,3}(?:\.[0-9]{3})*,[0-9]{2}$'
    return bool(re.match(pattern, value))

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to remove unsafe characters"""
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized[:255]