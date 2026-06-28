import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    return mo, pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Análise Exploratória de Vendas de Chocolate

    Vamos agora realizar uma análise exploratória das vendas de chocolate para o Brasil nos anos de 2022 e 2023, entender as sazonalidades, efeito do marketing sobre as vendas (incluindo o retorno) e oportunidades de investimento para a produção. A análise será dividida em 3 canais:

    - Atacado
    - Varejo
    - Vendas Online

    Os produtos analisados são de diversas marcas de uma chocolateria não especificada.

    ## Colunas do Dataset

    Nossas variáveis para trabalho são as seguintes:

    | Nome da Coluna | Tipo de Dado | Descrição |
    | :--- | :--- | :--- |
    | **Order_ID** | Texto / ID | Identificador único para cada pedido/transação. |
    | **Product** | Texto | Nome do produto de chocolate comercializado. |
    | **Country** | Texto | País onde a venda foi realizada. |
    | **Channel** | Texto | Canal de distribuição/vendas utilizado (**Retail** / Varejo, **Online** / E-commerce, **Wholesale** / Atacado). |
    | **Salesperson** | Texto | Nome do representante de vendas responsável pelo pedido. |
    | **Order_Date** | Data | Data em que o pedido foi efetuado pelo cliente. |
    | **Discount_Pct** | Numérico (%) | Percentual de desconto aplicado sobre o pedido. |
    | **Price_per_Box** | Numérico (USD) | Preço de cada caixa de chocolate, já deduzido o desconto. |
    | **Marketing_Spend** | Numérico (USD) | Orçamento de marketing alocado ou rateado para este pedido/período. |
    | **Boxes_Shipped** | Numérico (Inteiro) | Quantidade total de caixas enviadas para o pedido. |
    | **Amount** | Numérico (USD) | Faturamento total do pedido, calculado como: *Boxes_Shipped* × *Price_per_Box*. |

    ## Perguntas de Negócio

    #### 1. Performance de Canais e Produtos
    * **Q1:** Qual canal de vendas (`Channel`) gera o maior faturamento total (`Amount`) e qual vende o maior volume de caixas (`Boxes_Shipped`)?
    * **Q2:** Quais produtos (`Product`) são os mais vendidos em cada país (`Country`)? Existe preferência regional por algum tipo de chocolate?
    * **Q3:** Qual é a relação entre o desconto aplicado (`Discount_Pct`) e o volume de caixas vendidas? Descontos maiores de fato geram pedidos significativamente maiores?

    #### 2. Eficiência de Marketing e ROI
    * **Q4:** Qual é o Retorno sobre o Investimento em Marketing (ROI) por canal? Onde o `Marketing_Spend` está sendo mais eficiente para gerar faturamento (`Amount`)?
    * **Q5:** Existe um efeito de sazonalidade perceptível onde picos de `Marketing_Spend` são seguidos por picos de vendas (`Boxes_Shipped`) nas semanas seguintes?
    * **Q6:** Qual produto possui o maior custo de marketing proporcional ao seu faturamento total?

    #### 3. Sazonalidade e Tendências Temporais
    * **Q7:** Como o faturamento total oscila ao longo dos meses do ano? Conseguimos identificar picos claros de vendas (ex: Páscoa, Fim de Ano)?
    * **Q8:** A tendência de vendas do canal `Online` está crescendo a uma taxa maior do que os canais físicos (`Retail` e `Wholesale`) ao longo da série histórica?
    """)
    return


@app.cell
def _(pd):
    # importando os dados:

    dados_varejo = pd.read_csv("./data/silver/chocolate_varejo_2022_2023.csv")
    dados_varejo = dados_varejo.drop(columns=["Unnamed: 0", "Order_ID"])
    dados_atacado = pd.read_csv("./data/silver/chocolate_atacado_2022_2023.csv")
    dados_atacado = dados_atacado.drop(columns=["Unnamed: 0", "Order_ID"])
    dados_online = pd.read_csv("./data/silver/chocolate_online_2022_2023.csv")
    dados_online = dados_online.drop(columns=["Unnamed: 0", "Order_ID"])
    dados_online
    return dados_atacado, dados_online, dados_varejo


@app.cell
def _(plt, sns):
    # Configuração estética geral dos gráficos
    sns.set_theme(style="whitegrid")

    def plotar_serie_produto_especifico(df, produto, coluna_numerica='Boxes_Shipped', coluna_data='Order_Date', coluna_produto='Product'):
        """
        Gera um gráfico de linha detalhado para um único produto específico.
        """
        # Filtrar os dados apenas para o produto escolhido
        df_produto = df[df[coluna_produto] == produto].sort_values(by=coluna_data)

        if df_produto.empty:
            print(f"Produto '{produto}' não encontrado no dataset.")
            return

        plt.figure(figsize=(14, 6))

        # Desenhar a linha temporal
        sns.lineplot(data=df_produto, x=coluna_data, y=coluna_numerica, marker='o', color='#7A3E3F', linewidth=2)

        plt.title(f'Evolução Temporal de {coluna_numerica} - {produto}', fontsize=16, fontweight='bold', pad=15)
        plt.xlabel('Data do Pedido', fontsize=12)
        plt.ylabel(coluna_numerica, fontsize=12)
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()


    def plotar_comparativo_produtos(df, coluna_numerica='Boxes_Shipped', coluna_data='Order_Date', coluna_produto='Product'):
        """
        Gera um gráfico comparativo com todos os produtos do dataset para análise de share e tendência.
        """
        # Agrupar os dados por data e produto caso haja múltiplas vendas no mesmo dia (para o gráfico ficar limpo)
        df_agrupado = df.groupby([coluna_data, coluna_produto])[coluna_numerica].sum().reset_index()
        df_agrupado = df_agrupado.sort_values(by=coluna_data)

        plt.figure(figsize=(16, 7))

        # Criar linhas com cores diferentes para cada chocolate
        sns.lineplot(data=df_agrupado, x=coluna_data, y=coluna_numerica, hue=coluna_produto, palette='Dark2', linewidth=2)

        plt.title(f'Comparativo Temporal de {coluna_numerica} por Produto', fontsize=16, fontweight='bold', pad=15)
        plt.xlabel('Data do Pedido', fontsize=12)
        plt.ylabel(f'Total de {coluna_numerica}', fontsize=12)
        plt.xticks(rotation=45)

        # Ajustar a legenda para fora do gráfico para não cobrir as linhas
        plt.legend(title='Produtos', bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        plt.show()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Performance de Canais e Produtos

    Vamos às perguntas de negócios.

    **Q1:** Qual canal de vendas (`Channel`) gera o maior faturamento total (`Amount`) e qual vende o maior volume de caixas (`Boxes_Shipped`)?
    """)
    return


@app.cell
def _(dados_atacado, dados_online, dados_varejo):
    faturamento_online = dados_online["Amount"].sum()
    faturamento_varejo = dados_varejo["Amount"].sum()
    faturamento_atacado = dados_atacado["Amount"].sum()

    faturamento_online, faturamento_varejo, faturamento_atacado
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Como podemos observar, o varejo corresponde ao maior faturamento, com 22 milhões, seguido pelo atacado (15 milhões) e vendas online (4 milhões).
    """)
    return


@app.cell
def _(dados_atacado, dados_online, dados_varejo):
    # Investigando os volumes de caixas vendiads (assumindo que as caixas são de tamanho padrão)

    volume_online = dados_online["Boxes_Shipped"].sum()
    volume_atacado = dados_atacado["Boxes_Shipped"].sum()
    volume_varejo = dados_varejo["Boxes_Shipped"].sum()

    volume_online, volume_atacado, volume_varejo
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Novamente temos o varejo na liderança com 5 milhões de caixas, seguido pelo atacado com 3 milhões de caixas vendidas e pelas vendas online com 1 milhão de caixas vendidas.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2:** Quais produtos (`Product`) são os mais vendidos em cada país (`Country`)? Existe preferência regional por algum tipo de chocolate?
    """)
    return


@app.cell
def _(dados_online):
    # Como estamos focando nas análises de vendas do Brasil, precisamos avaliar os seguimentos e agrupar por produto. Vamos observar os retornos e os volumes para identificar preferencias

    # online

    retornos_online = dados_online.groupby("Product")["Amount"].sum().sort_values(ascending=False)
    volumes_online = dados_online.groupby("Product")["Boxes_Shipped"].sum().sort_values(ascending=False)
    return retornos_online, volumes_online


@app.cell
def _(retornos_online):
    retornos_online
    return


@app.cell
def _(volumes_online):
    volumes_online
    return


@app.cell
def _(dados_varejo):
    # varejo

    retornos_varejo = dados_varejo.groupby("Product")["Amount"].sum().sort_values(ascending=False)
    volumes_varejo = dados_varejo.groupby("Product")["Boxes_Shipped"].sum().sort_values(ascending=False)
    return retornos_varejo, volumes_varejo


@app.cell
def _(retornos_varejo):
    retornos_varejo
    return


@app.cell
def _(volumes_varejo):
    volumes_varejo
    return


@app.cell
def _(dados_atacado):
    # atacado

    retornos_atacado = dados_atacado.groupby("Product")["Amount"].sum().sort_values(ascending=False) 
    volumes_atacado = dados_atacado.groupby("Product")["Boxes_Shipped"].sum().sort_values(ascending=False)
    return retornos_atacado, volumes_atacado


@app.cell
def _(retornos_atacado):
    retornos_atacado
    return


@app.cell
def _(volumes_atacado):
    volumes_atacado
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Em geral o top 3 de produtos é bastante consistente: barras de chocolate 70%, truffle gift boxes e mixed assortment boxes (traduzir estes nomes). Estas consistentemente apresentam preferências regionais uma vez que os quartos produtos mais encomendados possuem demandas 3x menores aproximadamente.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3:** Qual é a relação entre o desconto aplicado (`Discount_Pct`) e o volume de caixas vendidas? Descontos maiores de fato geram pedidos significativamente maiores?
    """)
    return


@app.cell
def _(plt, sns):
    # vamos gerar scatter plots para os dias de venda relacionando o volume de caixas vendidas e as porcentagens de desconto de modo a procurar tendencias na nuvem de pontos. Vamos melhorar a observação de padrões a partir dos volumes de vendas mensais e do desconto médio aplicado naquele mês.

    def plot_dispersao(df, coluna_x, coluna_y, titulo_canal, cor="blue"):
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(9, 5))

        # Cria o scatter plot
        plt.scatter(df[coluna_x], df[coluna_y], color=cor, alpha=0.8, edgecolors="w")

        # Títulos dinâmicos incluindo o nome do canal (Online, Varejo, Atacado)
        plt.title(
            f"Dispersão ({titulo_canal}): {coluna_x} vs {coluna_y}",
            fontsize=13,
            fontweight="bold",
        )
        plt.xlabel(coluna_x, fontsize=11)
        plt.ylabel(coluna_y, fontsize=11)

        plt.show()

    return (plot_dispersao,)


@app.cell
def _(dados_atacado, dados_online, dados_varejo, pd, plot_dispersao):
    dataframes = {
        "Online": dados_online,
        "Varejo": dados_varejo,
        "Atacado": dados_atacado,
    }

    # Cores diferentes para diferenciar os gráficos de cada canal
    cores = {"Online": "royalblue", "Varejo": "darkorange", "Atacado": "forestgreen"}

    for nome, df in dataframes.items():
        # Garante a conversão da data
        df["Order_Date"] = pd.to_datetime(df["Order_Date"])

        # Agrupa por mês e calcula as métricas
        df_mensal = (
            df.groupby(df["Order_Date"].dt.to_period("M"))
            .agg(
                Desconto_Medio=("Discount_Pct", "mean"),
                Total_Boxes_Shipped=("Boxes_Shipped", "sum"),
            )
            .reset_index()
        )

        # Converte o período para string apenas para evitar avisos de compatibilidade no plot
        df_mensal["Order_Date"] = df_mensal["Order_Date"].astype(str)

        # Chame a função de scatter plot para o canal atual
        # Aqui estamos cruzando o Desconto Médio (X) com o Total de Caixas Enviadas (Y)
        plot_dispersao(
            df=df_mensal,
            coluna_x="Desconto_Medio",
            coluna_y="Total_Boxes_Shipped",
            titulo_canal=nome,
            cor=cores[nome],
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Aparentemente os descontos não afetam o volume de vendas de forma notável, sendo a nuvem de pontos praticamente aleatória. Isto significa que é totalmente possível aplicar descontos baixos para vender em volume garantindo uma maior margem de lucro sem machucar a base consumidora no processo.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Eficiência de Marketing e ROI

    Vamos às perguntas de negócios.

    **Q4:** Qual é o Retorno sobre o Investimento em Marketing (ROI) por canal? Onde o `Marketing_Spend` está sendo mais eficiente para gerar faturamento (`Amount`)?
    """)
    return


@app.cell
def _(dados_atacado, dados_online, dados_varejo, pd, plot_dispersao):
    def gerar_analise_marketing():
        canais_dados = {
            "Online": dados_online,
            "Varejo": dados_varejo,
            "Atacado": dados_atacado,
        }

        # Agora 'cores_locais', 'nome' e 'df_mensal' nascem e morrem aqui dentro
        cores_locais = {"Online": "purple", "Varejo": "crimson", "Atacado": "teal"}
        graficos_locais = {}

        for nome, df_original in canais_dados.items():
            df_com_data = df_original.assign(
                Order_Date_Parsed=pd.to_datetime(df_original["Order_Date"])
            )

            df_mensal = (
                df_com_data.groupby(df_com_data["Order_Date_Parsed"].dt.to_period("M"))
                .agg(
                    Total_Marketing=("Marketing_Spend", "sum"),
                    Total_Amount=("Amount", "sum"),
                )
                .reset_index()
            )

            df_plot = df_mensal.assign(
                Order_Date_Str=df_mensal["Order_Date_Parsed"].astype(str)
            )

            graficos_locais[nome] = plot_dispersao(
                df=df_plot,
                coluna_x="Total_Marketing",
                coluna_y="Total_Amount",
                titulo_canal=nome,
                cor=cores_locais[nome],
            )

        return graficos_locais


    # Executa a função e gera uma única variável global controlada pelo Marimo
    graficos_marketing = gerar_analise_marketing()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Todos os canais possuem um amento gradual nos faturamentos em relação às campanhas de marketing com ênfase especial ao segmento online, que registrou ganhos milionários. Isto é esperado pois os demais segmentos ganham muito com vendas passivas de pessoas que vão aos estabeleciomentos, enquanto as campanhas dinamicas de redes sociais trazem clientes pelas vias das vendas online.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5:** Existe um efeito de sazonalidade perceptível onde picos de `Marketing_Spend` são seguidos por picos de vendas (`Boxes_Shipped`) nas semanas seguintes?
    """)
    return


@app.cell
def _(dados_atacado, dados_online, dados_varejo, pd, plt, sns):
    # --- 1. Função Corrigida (Sem Avisos e Pronta para o Marimo) ---
    def plot_linha_temporal(df, titulo_canal, cor_marketing, cor_volume):
        sns.set_theme(style="whitegrid")

        fig, ax1 = plt.subplots(figsize=(10, 5))

        # Linha 1: Gastos com Marketing
        (linha1,) = ax1.plot(
            df["Order_Date_Str"],
            df["Total_Marketing"],
            color=cor_marketing,
            marker="o",
            linewidth=2,
            label="Gastos com Marketing",
        )
        ax1.set_xlabel("Meses", fontsize=11)
        ax1.set_ylabel("Total Marketing Spend ($)", color=cor_marketing, fontsize=11)
        ax1.tick_params(axis="y", labelcolor=cor_marketing)

        # Cria o segundo eixo
        ax2 = ax1.twinx()

        # Linha 2: Caixas Enviadas
        (linha2,) = ax2.plot(
            df["Order_Date_Str"],
            df["Total_Boxes"],
            color=cor_volume,
            marker="s",
            linewidth=2,
            linestyle="--",
            label="Caixas Enviadas",
        )
        ax2.set_ylabel("Total Boxes Shipped", color=cor_volume, fontsize=11)
        ax2.tick_params(axis="y", labelcolor=cor_volume)

        # --- CORREÇÃO DO AVISO AQUI ---
        # Primeiro dizemos ONDE ficam os ticks (as posições de 0 até o fim do dataframe)
        ax1.set_xticks(range(len(df["Order_Date_Str"])))
        # Depois aplicamos os textos com segurança
        ax1.set_xticklabels(df["Order_Date_Str"], rotation=45, ha="right")

        # Junta as legendas
        linhas = [linha1, linha2]
        legendas = [l.get_label() for l in linhas]
        ax1.legend(linhas, legendas, loc="upper left")

        ax1.set_title(
            f"Evolução Temporal ({titulo_canal}): Marketing vs Volumes",
            fontsize=13,
            fontweight="bold",
        )
        fig.tight_layout()

        # Importante fechar para não duplicar na memória do matplotlib,
        # mas retornamos o objeto fig para o Marimo renderizar
        plt.close(fig)
        return fig


    # --- 2. Processamento ---
    def gerar_analise_temporal():
        canais_dados = {
            "Online": dados_online,
            "Varejo": dados_varejo,
            "Atacado": dados_atacado,
        }

        cores_canais = {
            "Online": ("purple", "orchid"),
            "Varejo": ("crimson", "salmon"),
            "Atacado": ("teal", "mediumturquoise"),
        }

        graficos_linhas_locais = {}

        for nome, df_original in canais_dados.items():
            df_com_data = df_original.assign(
                Order_Date_Parsed=pd.to_datetime(df_original["Order_Date"])
            )

            df_mensal = (
                df_com_data.groupby(df_com_data["Order_Date_Parsed"].dt.to_period("M"))
                .agg(
                    Total_Marketing=("Marketing_Spend", "sum"),
                    Total_Boxes=("Boxes_Shipped", "sum"),
                )
                .reset_index()
            )

            df_mensal = df_mensal.sort_values("Order_Date_Parsed")
            df_plot = df_mensal.assign(
                Order_Date_Str=df_mensal["Order_Date_Parsed"].astype(str)
            )

            cor_mkt, cor_box = cores_canais[nome]

            graficos_linhas_locais[nome] = plot_linha_temporal(
                df=df_plot,
                titulo_canal=nome,
                cor_marketing=cor_mkt,
                cor_volume=cor_box,
            )

        return graficos_linhas_locais


    # Executa
    graficos_temporais = gerar_analise_temporal()

    # --- PARA PLOTAR NO MARIMO ---
    # Chame as chaves do dicionário no final da célula para elas aparecerem na tela:
    graficos_temporais
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Não foram observados grandes impactos do investimento de marketing nos volumes vendidos. Isso pode representar uma base consolidada com demandas regulares pelos produtos, com baixo potencial explosivo. Nesses casos, o marketing pode se concentrar em lembrar os clientes da existência da marca para garantir fluxo constante de receita apostando em campeões e explorar novas bases consumidoras com produtos que possuam margem para abertura.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6:** Qual produto possui o maior custo de marketing proporcional ao seu faturamento total?
    """)
    return


@app.cell
def _(dados_atacado, dados_online, dados_varejo, plt, sns):
    # --- 1. Função Visual de Ranking ---
    def plot_ranking_eficiencia(df, titulo_canal, mapa_cores="viridis"):
        sns.set_theme(style="whitegrid")

        # Criamos a figura
        fig, ax = plt.subplots(figsize=(10, 6))

        # Criando o gráfico de barras horizontais
        # Usamos o 'Retorno_Por_Investimento' para definir a cor (hue) e criar um efeito degradê bonito
        barplot = sns.barplot(
            data=df,
            x="Retorno_Por_Investimento",
            y="Product",
            hue="Retorno_Por_Investimento",
            palette=mapa_cores,
            legend=False,
            ax=ax,
        )

        # Adiciona os valores numéricos escritos na ponta de cada barra
        for container in ax.containers:
            ax.bar_label(
                container, fmt="%.1fx", padding=5, fontsize=10, weight="bold"
            )

        # Customização estética dos eixos e títulos
        ax.set_title(
            f"Ranking de Eficiência de Marketing ({titulo_canal})\nRetorno em Receita para cada $1 investido",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )
        ax.set_xlabel("Taxa de Retorno (Receita / Investimento)", fontsize=11)
        ax.set_ylabel("Produtos", fontsize=11)

        # Limpa as bordas para um visual minimalista
        sns.despine(left=True, bottom=True)

        fig.tight_layout()
        plt.close(fig)
        return fig


    # --- 2. Processamento e Geração de Todos os Gráficos ---
    def analisar_e_plotar_rankings():
        canais_dados = {
            "Online": dados_online,
            "Varejo": dados_varejo,
            "Atacado": dados_atacado,
        }

        # Paletas de cores diferentes para cada gráfico ficar único e bonito
        paletas = {"Online": "Purples_r", "Varejo": "Reds_r", "Atacado": "crest_r"}

        visualizacoes_locais = {}

        for nome, df_original in canais_dados.items():
            # Agrupa e soma as métricas essenciais por produto
            df_produto = (
                df_original.groupby("Product")
                .agg(
                    Receita_Total=("Amount", "sum"),
                    Marketing_Total=("Marketing_Spend", "sum"),
                )
                .reset_index()
            )

            # Calcula o ROI (Retorno por Investimento)
            df_roi = df_produto.assign(
                Retorno_Por_Investimento=df_produto["Receita_Total"]
                / df_produto["Marketing_Total"]
            )

            # Filtra produtos que não tiveram gasto de marketing para evitar divisão por zero ou infinito
            df_roi = df_roi[df_roi["Marketing_Total"] > 0]

            # Pega o Top 10 produtos mais eficientes para o gráfico não ficar gigante e poluído
            df_top10 = df_roi.sort_values(
                by="Retorno_Por_Investimento", ascending=False
            ).head(10)

            # Gera o gráfico visual chamando a nossa função técnica
            visualizacoes_locais[nome] = plot_ranking_eficiencia(
                df=df_top10, titulo_canal=nome, mapa_cores=paletas[nome]
            )

        return visualizacoes_locais


    # Executa com segurança no Marimo
    graficos_ranking = analisar_e_plotar_rankings()

    # --- EXIBIÇÃO NO MARIMO ---
    # Chame o dicionário para ver todos renderizados na célula, ou chame um por um:
    graficos_ranking
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Podemos observar que nos 3 segmentos as caixas sortidas de chocolates fazem um tremendo sucesso, com a receita chegando a mais de 10x o valor investido nas campanhas de marketing. Isso mostra que, como os produtos são bem queridos de modo geral (embora existam preferidos claramente delimitados), o público ainda gosta muito do fator surpresa de descobrir novos e a possibilidade de ganhar mimos dos campeões dentre as possibilidades.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sazonalidade e Tendências Temporais

    Vamos às perguntas de negócios.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7:** Como o faturamento total oscila ao longo dos meses do ano? Conseguimos identificar picos claros de vendas (ex: Páscoa, Fim de Ano)?
    """)
    return


@app.cell
def _(dados_atacado, dados_online, dados_varejo, pd, plt, sns):
    # --- 1. Função Visual de Faturamento ---
    def plot_faturamento_temporal(df, titulo_canal, cor_linha):
        sns.set_theme(style="whitegrid")

        fig, ax = plt.subplots(figsize=(10, 5))

        # Plota a linha de faturamento puro
        ax.plot(
            df["Order_Date_Str"],
            df["Total_Amount"],
            color=cor_linha,
            marker="o",
            linewidth=2.5,
            label="Faturamento (Amount)",
        )

        # Configurações de eixos e títulos
        ax.set_title(
            f"Evolução do Faturamento Mensal ({titulo_canal})",
            fontsize=13,
            fontweight="bold",
            pad=12,
        )
        ax.set_xlabel("Meses", fontsize=11)
        ax.set_ylabel("Faturamento Total ($)", fontsize=11)

        # Evita o erro de ticks desalinhados no Marimo
        ax.set_xticks(range(len(df["Order_Date_Str"])))
        ax.set_xticklabels(df["Order_Date_Str"], rotation=45, ha="right")

        ax.legend(loc="upper left")
        fig.tight_layout()

        plt.close(fig)
        return fig


    # --- 2. Processamento Limpo para o Marimo ---
    def gerar_linha_faturamento():
        canais_dados = {
            "Online": dados_online,
            "Varejo": dados_varejo,
            "Atacado": dados_atacado,
        }

        # Cores exclusivas para destacar cada linha de canal
        cores = {"Online": "indigo", "Varejo": "darkred", "Atacado": "teal"}

        graficos_faturamento_locais = {}

        for nome, df_original in canais_dados.items():
            # Converte sem mutar a variável de outras células
            df_com_data = df_original.assign(
                Order_Date_Parsed=pd.to_datetime(df_original["Order_Date"])
            )

            # Agrupa pelo período mensal e soma o faturamento
            df_mensal = (
                df_com_data.groupby(df_com_data["Order_Date_Parsed"].dt.to_period("M"))
                .agg(Total_Amount=("Amount", "sum"))
                .reset_index()
            )

            # Garante a ordem cronológica correta
            df_mensal = df_mensal.sort_values("Order_Date_Parsed")

            # Converte para string para a plotagem
            df_plot = df_mensal.assign(
                Order_Date_Str=df_mensal["Order_Date_Parsed"].astype(str)
            )

            # Gera o gráfico limpo
            graficos_faturamento_locais[nome] = plot_faturamento_temporal(
                df=df_plot, titulo_canal=nome, cor_linha=cores[nome]
            )

        return graficos_faturamento_locais


    # Executa
    graficos_faturamento = gerar_linha_faturamento()

    # --- EXIBIÇÃO NO MARIMO ---
    # Só chamar o dicionário ou o canal desejado para renderizar:
    graficos_faturamento
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As vendas de chocolate no Brasil para a marca em questão atingem picos históricos no fim de ano. Na páscoa há picos locais.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8:** A tendência de vendas do canal `Online` está crescendo a uma taxa maior do que os canais físicos (`Retail` e `Wholesale`) ao longo da série histórica?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Os faturamentos estão estáveis como pode ser inferido ao longo da análise pela base de clientes fixa.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
