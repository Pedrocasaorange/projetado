import os

SECRET_KEY = 'Chave_segurança_projetado_2025'
DATA_FILE = 'fluxo_caixa_dados.json'

EMPREENDIMENTOS = [
    "ALLEGRO",
    "PIAZZA",
    "CASA PARQUE",
    "CASA BOA VIAGEM", 
    "CASA MAYOR",
    "CASA ORIZON",
    "CASA DO POÇO",
    "CASA MAR"
]

USUARIOS = {
    'Legalização': {'senha': 'legalização2025', 'setor': 'legalizacao'},
    'obra':        {'senha': 'Obra2025', 'setor': 'obra'},
    'Projetos':    {'senha': 'Projetos2025', 'setor': 'projeto'},
    'marketing':   {'senha': 'Marketing2025', 'setor': 'marketing'},
    'Produtos':    {'senha': 'Produtos2025', 'setor': 'produtos'}, 
    'Pos obra':    {'senha': 'Pos-obra2025', 'setor': 'pos_obra'},
    'ADM':         {'senha': 'C2025asaOrange', 'setor': 'admin'}
}