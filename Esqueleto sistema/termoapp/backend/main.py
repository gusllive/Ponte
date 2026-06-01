import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.component import Componente
from services.calculadora import CalculadoraTermodinamica

app = FastAPI(title="API Termodinâmica Química")

# Permite que o Flutter acesse a API sem bloqueios de segurança de navegador (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CARREGAMENTO DO BANCO DE DADOS PICKLE ---
# Como main.py está na pasta 'backend', os arquivos estão na pasta irmã 'app/data' ou dentro de 'backend/data' dependendo de onde salvou.
# Ajustamos para buscar na pasta correta baseada no seu primeiro print: 'app/backend/app/data' não existe, o correto é subir um nível ou ir direto a 'data'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_DATA = os.path.join(BASE_DIR, "data") 

tabelas_lee_kesler = {}
banco_componentes = {}
@app.on_event("startup")
def carregar_banco_dados():
    global tabelas_lee_kesler, banco_componentes
    try:
        print(f"🔎 Procurando arquivos Pickle em: {PATH_DATA}")
        
        # 1. Carregando tabelas do Lee Kesler
        tabelas_lee_kesler['Z0'] = pd.read_pickle(os.path.join(PATH_DATA, 'Z_Lee_Kesler_Z0_dados.pickle'))
        tabelas_lee_kesler['Z1'] = pd.read_pickle(os.path.join(PATH_DATA, 'Z_Lee_Kesler_Z1_dados.pickle'))
        tabelas_lee_kesler['Pr'] = pd.read_pickle(os.path.join(PATH_DATA, 'Z_Lee_Kesler_Pr_dados.pickle'))
        
        # 2. Carregando o banco geral de propriedades puras
        dados_prop = pd.read_pickle(os.path.join(PATH_DATA, 'databank_properties.pickle'))
        
        # SE FOR UM DATAFRAME DO PANDAS:
        if isinstance(dados_prop, pd.DataFrame):
            print("📊 Identificado: databank_properties é um DataFrame Pandas.")
            for _, row in dados_prop.iterrows():
                nome_comp = str(row['nome']).lower().strip()
                banco_componentes[nome_comp] = Componente(
                    nome=row['nome'], Tc=row['Tc'], Pc=row['Pc'], omega=row['omega']
                )
                
        # SE FOR UMA LISTA DE DICIONÁRIOS (O seu caso atual!):
        elif isinstance(dados_prop, list):
            print(f"📋 Identificado: databank_properties é uma Lista com {len(dados_prop)} itens.")
            for item in dados_prop:
                # Se cada item da lista for um dicionário {'nome': ..., 'Tc': ...}
                if isinstance(item, dict):
                    nome_comp = str(item.get('nome', '')).lower().strip()
                    banco_componentes[nome_comp] = Componente(
                        nome=item.get('nome', 'Desconhecido'),
                        Tc=float(item.get('Tc', 0)),
                        Pc=float(item.get('Pc', 0)),
                        omega=float(item.get('omega', 0))
                    )
                # Se for uma lista de objetos do próprio tipo Componente salvos diretamente
                elif hasattr(item, 'nome') or hasattr(item, 'Tc'):
                    nome_comp = str(item.nome).lower().strip()
                    banco_componentes[nome_comp] = Componente(
                        nome=item.nome, Tc=item.Tc, Pc=item.Pc, omega=item.omega
                    )
        
        print(f"⚡ {len(banco_componentes)} componentes carregados com sucesso na RAM!")
        
    except Exception as e:
        print(f"❌ Erro ao carregar arquivos Pickle: {e}")
# --- ROTAS DA API ---

@app.get("/componentes")
def listar_componentes():
    """Retorna a lista de nomes disponíveis no banco para preencher o Dropdown no Flutter"""
    return {"componentes": [c.nome for c in banco_componentes.values()]}

@app.get("/calcular/pitzer")
def calcular_pitzer(comp: str, t: float, p: float):
    componente = banco_componentes.get(comp.lower().strip())
    if not componente:
        raise HTTPException(status_code=404, detail="Componente não encontrado.")
    
    calc = CalculadoraTermodinamica(componente)
    return calc.calcular_Z_Pitzer_2c(t, p)

@app.get("/calcular/lee-kesler")
def calcular_lee_kesler(comp: str, t: float, p: float):
    componente = banco_componentes.get(comp.lower().strip())
    if not componente:
        raise HTTPException(status_code=404, detail="Componente não encontrado.")
        
    calc = CalculadoraTermodinamica(componente)
    return calc.calcular_Z_Lee_Kesler(t, p, tabelas_lee_kesler)