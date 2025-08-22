import pandas as pd
import os
import glob 
from log import log_decorator
#Função de extract que ler e consolida os arquivos json

@log_decorator
def extrair_dados_e_consolidar(path: str) -> pd.DataFrame:

    arquivos_json = glob.glob(os.path.join(path, "*.json" ))
    df_list = [pd.read_json(arquivo) for arquivo in arquivos_json]
    df_total = pd.concat(df_list, ignore_index=True)
    return df_total

# Função de Transformação
@log_decorator
def calcular_total_vendas(df: pd.DataFrame) -> pd.DataFrame:
    df["Total"] = df["Quantidade"] * df["Venda"]
    return df

# Função para carregar os dados nos formatos CSV ou Parquet
@log_decorator
def carregar_dados(df: pd.DataFrame, formato_de_saida: list):
    """
    Esta função vai receber um parametro csv ou parquet ou os dois
    """
    for formato in formato_de_saida:
        if formato  == "csv":
            df.to_csv("dados.csv", index=False)
        if formato == "parquet":
            df.to_parquet("dados.parquet", index=False)

@log_decorator
def pipeline_calcular_vendas_consolidado(pasta: str, formato_de_saida:list):
    data_frame = extrair_dados_e_consolidar(pasta)
    data_frame_calculado = calcular_total_vendas(data_frame)
    carregar_dados(data_frame_calculado, formato_de_saida)