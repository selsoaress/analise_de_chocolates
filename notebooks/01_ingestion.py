import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    return mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Processamento Inicial de Dados

    Este projeto busca construir relatórios e extrair insights sobre vendas de chocolates entre os anos 2022 e 2023.
    """)
    return


@app.cell
def _(pd):
    dados_brutos = pd.read_csv("./data/bronze/Chocolate_Sales.csv")
    dados_brutos
    return (dados_brutos,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Nossa análise se concentrará na sazonalidade e nos efeitos da publicidade sobre as compras de chocolate. Vamos concentrar nossa análise em dados anonimizados em termos dos vendedores no Brasil para entender o nosso mercado consumidor e identificar oportunidades.

    Podemos observar que há dados faltantes. Por se tratarem de dados com datas, podemos utilizar uma suavização com média móvel ao longo da série temporal de modo a preencher lacunas sem ignorar o contexto sazonal das variáveis em questão.
    """)
    return


@app.cell
def _(pd):
    def preencher_tudo_na_estrutura_original(df, coluna_data='Order_Date', coluna_produto='Product', colunas_numericas=None, janela=30):
        """
        Mantém a estrutura original do DataFrame intacta (mesmo número de linhas).
        Aproxima datas nulas usando os registros vizinhos mais próximos,
        corrige formatos de data mistos e preenche valores numéricos nulos com média móvel.
        """
        df_clean = df.copy()

        # 1. TRATAMENTO DAS DATAS FALTANTES E INCONSISTENTES
        # Primeiro, tentamos converter o que já existe para datetime (tratando o erro de formatos mistos)
        df_clean[coluna_data] = pd.to_datetime(df_clean[coluna_data], format='mixed', dayfirst=True, errors='coerce')

        # Agora aproximamos as DATAS que estavam nulas usando os vizinhos mais próximos (anterior e depois posterior)
        df_clean[coluna_data] = df_clean[coluna_data].ffill().bfill()

        # 2. ORDENAÇÃO CRONOLÓGICA
        # Com todas as datas preenchidas e válidas, podemos ordenar o dataset com segurança
        df_clean = df_clean.sort_values(by=coluna_data).reset_index(drop=True)

        # 3. TRATAMENTO DAS COLUNAS NUMÉRICAS
        if colunas_numericas is None:
            colunas_numericas = ['Boxes_Shipped', 'Marketing_Spend', 'Price_per_Box', 'Discount_Pct']

        for col in colunas_numericas:
            if col in df_clean.columns:
                # Garante que a coluna é numérica
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

                # Calcula a média móvel baseada nos registros existentes do mesmo produto
                media_movel = df_clean.groupby(coluna_produto)[col].transform(
                    lambda x: x.rolling(window=janela, min_periods=1).mean()
                )

                # Preenche os nulos da coluna numérica com a média móvel
                df_clean[col] = df_clean[col].fillna(media_movel)

                # Backup: se ainda restarem nulos no início do histórico, usa a média geral do produto
                media_geral_produto = df_clean.groupby(coluna_produto)[col].transform('mean')
                df_clean[col] = df_clean[col].fillna(media_geral_produto).fillna(0)

        # 4. RECALCULAR O FATURAMENTO (Amount)
        if 'Boxes_Shipped' in df_clean.columns and 'Price_per_Box' in df_clean.columns:
            df_clean['Amount'] = df_clean['Boxes_Shipped'] * df_clean['Price_per_Box']

        return df_clean

    return (preencher_tudo_na_estrutura_original,)


@app.cell
def _(dados_brutos, preencher_tudo_na_estrutura_original):
    dados_com_data = preencher_tudo_na_estrutura_original(dados_brutos)
    dados_com_data
    return (dados_com_data,)


@app.cell
def _(dados_com_data):
    dados_brasil = dados_com_data.drop(columns=["Salesperson"])
    dados_brasil = dados_brasil[dados_brasil["Country"] == "Brazil"]
    dados_brasil = dados_brasil.drop(columns=["Country"])
    dados_brasil
    return (dados_brasil,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note que temos quase 53 mil vendas para o mercado brasileiro! Vamos subdividir as vendas de chocolate em canais: Varejo, atacado e e-commerce.
    """)
    return


@app.cell
def _(dados_brasil):
    dados_varejo = dados_brasil[dados_brasil["Channel"] == "Retail"]
    dados_varejo = dados_varejo.drop(columns=["Channel"])

    dados_atacado = dados_brasil[dados_brasil["Channel"] == "Wholesale"]
    dados_atacado = dados_atacado.drop(columns=["Channel"])

    dados_online = dados_brasil[dados_brasil["Channel"] == "Online"]
    dados_online = dados_online.drop(columns=["Channel"])
    return dados_atacado, dados_online, dados_varejo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Por fim, vamos salvar os arquivos no diretório silver, pois já estão prontos para análises exploratórias.
    """)
    return


@app.cell
def _(dados_atacado, dados_online, dados_varejo):
    dados_varejo.to_csv("./data/silver/chocolate_varejo_2022_2023.csv")
    dados_atacado.to_csv("./data/silver/chocolate_atacado_2022_2023.csv")
    dados_online.to_csv("./data/silver/chocolate_online_2022_2023.csv")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
