import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Análise de Vendas · Chocolateria",
    page_icon="🍫",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# PALETA & ESTILOS
# ─────────────────────────────────────────────
CORES = {
    "crimson_escuro": "#2C1518",
    "borgonha":       "#6B1A1A",
    "vermelho":       "#C0201F",
    "vermelho_medio": "#D83A2A",
    "vermelho_vivo":  "#F02B1D",
    "chocolate":      "#3B1A0F",
    "cacau":          "#5C2E0E",
    "caramelo":       "#8B4513",
    "ouro_queimado":  "#B5651D",
    "baunilha":       "#F5E6D3",
    "creme":          "#FAF0E6",
    "fundo":          "#1A0A08",
    "card":           "#231210",
    "texto":          "#F5E6D3",
    "texto_muted":    "#C4A882",
}

CANAL_CORES = {
    "Varejo":  CORES["vermelho"],
    "Online":  CORES["caramelo"],
    "Atacado": CORES["borgonha"],
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {CORES['fundo']};
    color: {CORES['texto']};
}}

.stApp {{
    background-color: {CORES['fundo']};
    max-width: 860px;
    margin: 0 auto;
}}

/* Remove sidebar */
[data-testid="stSidebar"] {{ display: none; }}
[data-testid="collapsedControl"] {{ display: none; }}
header[data-testid="stHeader"] {{ background: transparent; }}

/* Títulos principais */
h1 {{
    font-family: 'Playfair Display', serif !important;
    font-size: 3rem !important;
    font-weight: 700 !important;
    color: {CORES['texto']} !important;
    line-height: 1.1 !important;
    margin-bottom: 0.25rem !important;
}}

h2 {{
    font-family: 'Playfair Display', serif !important;
    font-size: 1.7rem !important;
    font-weight: 400 !important;
    font-style: italic !important;
    color: {CORES['texto_muted']} !important;
    border-bottom: 1px solid {CORES['borgonha']}44 !important;
    padding-bottom: 0.5rem !important;
    margin-top: 3rem !important;
}}

h3 {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: {CORES['vermelho_medio']} !important;
    margin-bottom: 0.3rem !important;
}}

p, li {{
    color: {CORES['texto_muted']} !important;
    font-size: 0.95rem !important;
    line-height: 1.75 !important;
}}

/* Cards de métrica */
.metric-card {{
    background: linear-gradient(135deg, {CORES['card']} 0%, {CORES['chocolate']} 100%);
    border: 1px solid {CORES['borgonha']}55;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    text-align: center;
}}

.metric-value {{
    font-family: 'Playfair Display', serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: {CORES['texto']};
    line-height: 1;
    margin-bottom: 0.25rem;
}}

.metric-label {{
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {CORES['texto_muted']};
}}

.metric-delta {{
    font-size: 0.8rem;
    color: {CORES['caramelo']};
    margin-top: 0.2rem;
}}

/* Separador ornamental */
.ornament {{
    text-align: center;
    color: {CORES['borgonha']};
    font-size: 1.1rem;
    letter-spacing: 0.6em;
    margin: 2rem 0;
    opacity: 0.6;
}}

/* Insight box */
.insight {{
    background: {CORES['card']};
    border-left: 3px solid {CORES['vermelho']};
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.4rem;
    margin: 1.2rem 0;
}}

.insight p {{
    margin: 0 !important;
    font-size: 0.9rem !important;
    color: {CORES['baunilha']} !important;
}}

/* Hero strip */
.hero-strip {{
    background: linear-gradient(135deg, {CORES['chocolate']} 0%, {CORES['borgonha']} 50%, {CORES['crimson_escuro']} 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}}

.hero-strip::before {{
    content: "🍫";
    position: absolute;
    right: 1.5rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 4rem;
    opacity: 0.15;
}}

.hero-eyebrow {{
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: {CORES['caramelo']};
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

/* Tabela estilizada */
.stDataFrame {{ border-radius: 8px; overflow: hidden; }}

/* Plotly charts */
.js-plotly-plot .plotly {{ border-radius: 12px; }}

/* Remove streamlit branding */
#MainMenu, footer, .stDeployButton {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LEITURA DOS DADOS
# ─────────────────────────────────────────────
dados_varejo  = pd.read_csv("./data/silver/chocolate_varejo_2022_2023.csv")
dados_varejo  = dados_varejo.drop(columns=[c for c in ["Unnamed: 0", "Order_ID"] if c in dados_varejo.columns])

dados_atacado = pd.read_csv("./data/silver/chocolate_atacado_2022_2023.csv")
dados_atacado = dados_atacado.drop(columns=[c for c in ["Unnamed: 0", "Order_ID"] if c in dados_atacado.columns])

dados_online  = pd.read_csv("./data/silver/chocolate_online_2022_2023.csv")
dados_online  = dados_online.drop(columns=[c for c in ["Unnamed: 0", "Order_ID"] if c in dados_online.columns])

for df in [dados_varejo, dados_atacado, dados_online]:
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

dados_todos = pd.concat([dados_varejo, dados_online, dados_atacado], ignore_index=True)


# ─────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────
def fmt_brl(v, milhar=True):
    if v >= 1_000_000:
        return f"R$ {v/1_000_000:.1f}M"
    if milhar and v >= 1_000:
        return f"R$ {v/1_000:.0f}k"
    return f"R$ {v:,.0f}"

def fmt_num(v):
    if v >= 1_000_000:
        return f"{v/1_000_000:.1f}M"
    if v >= 1_000:
        return f"{v/1_000:.0f}k"
    return f"{v:,.0f}"

def insight_box(texto):
    st.markdown(f'<div class="insight"><p>{texto}</p></div>', unsafe_allow_html=True)

LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color=CORES["texto_muted"], size=12),
    margin=dict(l=0, r=0, t=40, b=0),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color=CORES["texto_muted"]),
        bordercolor="rgba(107,26,26,0.27)",
        borderwidth=1,
    ),
)

def estilizar(fig, titulo=""):
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text=titulo, font=dict(
            family="Playfair Display, serif",
            size=16,
            color=CORES["texto"],
        )) if titulo else None,
        xaxis=dict(
            gridcolor="rgba(107,26,26,0.13)",
            linecolor="rgba(107,26,26,0.27)",
            tickfont=dict(color=CORES["texto_muted"]),
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor="rgba(107,26,26,0.13)",
            linecolor="rgba(0,0,0,0)",
            tickfont=dict(color=CORES["texto_muted"]),
            zeroline=False,
        ),
    )
    return fig


# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-strip">
  <div class="hero-eyebrow">Brasil · 2022 – 2023</div>
  <h1 style="color:#F5E6D3;font-family:'Playfair Display',serif;font-size:2.4rem;margin:0;font-weight:700;">
    Análise Exploratória<br>de Vendas de Chocolate
  </h1>
  <p style="color:#C4A882;margin-top:0.75rem;font-size:0.9rem;max-width:480px;">
    Performance de canais, eficiência de marketing e sazonalidade para os anos de 2022 e 2023.
  </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MÉTRICAS GERAIS
# ─────────────────────────────────────────────
fat_varejo  = dados_varejo["Amount"].sum()
fat_online  = dados_online["Amount"].sum()
fat_atacado = dados_atacado["Amount"].sum()
fat_total   = fat_varejo + fat_online + fat_atacado

vol_varejo  = dados_varejo["Boxes_Shipped"].sum()
vol_online  = dados_online["Boxes_Shipped"].sum()
vol_atacado = dados_atacado["Boxes_Shipped"].sum()
vol_total   = vol_varejo + vol_online + vol_atacado

c1, c2, c3 = st.columns(3)
for col, label, valor in [
    (c1, "Faturamento Total", fmt_brl(fat_total)),
    (c2, "Caixas Vendidas",   fmt_num(vol_total)),
    (c3, "Canais Ativos",     "3"),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-value">{valor}</div>
          <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="ornament">· · ·</div>', unsafe_allow_html=True)

# Sobre o dataset
st.markdown("### Sobre o Dataset")
st.markdown("""
Esta análise cobre as vendas de chocolate no Brasil em **2022–2023**, distribuídas em três canais:
**Atacado**, **Varejo** e **Vendas Online**. As principais variáveis trabalhadas são faturamento (`Amount`),
volume de caixas (`Boxes_Shipped`), desconto aplicado (`Discount_Pct`), e investimento em marketing
(`Marketing_Spend`).
""")


# ─────────────────────────────────────────────
# SEÇÃO 1 · CANAIS E PRODUTOS
# ─────────────────────────────────────────────
st.markdown("## Performance de Canais e Produtos")

# Q1 — Faturamento e volume por canal
st.markdown("### Q1 · Faturamento e Volume por Canal")

canais   = ["Varejo", "Online", "Atacado"]
faturam  = [fat_varejo, fat_online, fat_atacado]
volumes  = [vol_varejo, vol_online, vol_atacado]
cores_c  = [CORES["vermelho"], CORES["caramelo"], CORES["borgonha"]]

fig_q1 = make_subplots(rows=1, cols=2, subplot_titles=["Faturamento (R$)", "Volume (caixas)"])

fig_q1.add_trace(go.Bar(
    x=canais, y=faturam,
    marker=dict(color=cores_c, line=dict(width=0)),
    text=[fmt_brl(v) for v in faturam],
    textposition="outside",
    textfont=dict(color=CORES["texto"], size=11),
    showlegend=False,
), row=1, col=1)

fig_q1.add_trace(go.Bar(
    x=canais, y=volumes,
    marker=dict(color=[f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.73)" for c in cores_c], line=dict(width=0)),
    text=[fmt_num(v) for v in volumes],
    textposition="outside",
    textfont=dict(color=CORES["texto"], size=11),
    showlegend=False,
), row=1, col=2)

fig_q1.update_layout(
    **LAYOUT_BASE,
    height=320,
)
for i in [1, 2]:
    fig_q1.update_xaxes(
        gridcolor="rgba(0,0,0,0)", linecolor="rgba(107,26,26,0.27)",
        tickfont=dict(color=CORES["texto_muted"]), row=1, col=i,
    )
    fig_q1.update_yaxes(
        gridcolor="rgba(107,26,26,0.13)", linecolor="rgba(0,0,0,0)",
        tickfont=dict(color=CORES["texto_muted"]), row=1, col=i,
    )
for ann in fig_q1.layout.annotations:
    ann.font.color = CORES["texto_muted"]
    ann.font.size = 11

st.plotly_chart(fig_q1, use_container_width=True)

insight_box(
    "O <strong>Varejo</strong> lidera com ~R$ 22M em faturamento e ~5M caixas — quase o dobro do Atacado "
    "(~R$ 15M / 3M caixas). O Online ainda representa uma fatia menor (~R$ 4M), mas com potencial de crescimento "
    "dado o baixo custo de distribuição."
)

# Q2 — Produtos por canal
st.markdown("### Q2 · Produtos Mais Vendidos por Canal")

fig_q2 = go.Figure()
for canal, df_c, cor in [
    ("Varejo",  dados_varejo,  CORES["vermelho"]),
    ("Online",  dados_online,  CORES["caramelo"]),
    ("Atacado", dados_atacado, CORES["borgonha"]),
]:
    top = df_c.groupby("Product")["Amount"].sum().nlargest(9).reset_index()
    fig_q2.add_trace(go.Bar(
        name=canal,
        x=top["Product"],
        y=top["Amount"],
        marker_color=cor,
        visible=(canal == "Varejo"),
    ))

dropdown = []
for i, canal in enumerate(["Varejo", "Online", "Atacado"]):
    vis = [i == j for j in range(3)]
    dropdown.append(dict(
        label=canal,
        method="update",
        args=[{"visible": vis}, {"title": f"Top Produtos · {canal}"}],
    ))

fig_q2.update_layout(
    **LAYOUT_BASE,
    height=360,
    updatemenus=[dict(
        buttons=dropdown,
        direction="right",
        x=0, xanchor="left", y=1.18, yanchor="top",
        bgcolor=CORES["card"],
        bordercolor=CORES["borgonha"],
        font=dict(color=CORES["texto_muted"]),
        showactive=True,
        type="buttons",
    )],
    xaxis=dict(
        tickangle=-35,
        gridcolor="rgba(0,0,0,0)",
        linecolor="rgba(107,26,26,0.27)",
        tickfont=dict(color=CORES["texto_muted"], size=10),
    ),
    yaxis=dict(
        gridcolor="rgba(107,26,26,0.13)",
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(color=CORES["texto_muted"]),
        tickprefix="R$ ",
    ),
)
st.plotly_chart(fig_q2, use_container_width=True)

insight_box(
    "O Top 3 é consistente nos três canais: <strong>Chocolate 70% Cacau</strong>, <strong>Truffle Gift Box</strong> "
    "e <strong>Mixed Assortment Box</strong>. Os produtos do 4º lugar em diante apresentam demanda ~3× menor, "
    "sinalizando uma concentração clara de preferências."
)

# Q3 — Desconto × Volume
st.markdown("### Q3 · Desconto vs. Volume de Caixas")

fig_q3 = go.Figure()
for canal, df_c, cor in [
    ("Varejo",  dados_varejo,  CORES["vermelho"]),
    ("Online",  dados_online,  CORES["caramelo"]),
    ("Atacado", dados_atacado, CORES["borgonha"]),
]:
    df_c2 = df_c.copy()
    df_c2["Order_Date"] = pd.to_datetime(df_c2["Order_Date"])
    mensal = (
        df_c2.groupby(df_c2["Order_Date"].dt.to_period("M"))
        .agg(Desconto_Medio=("Discount_Pct", "mean"), Total_Boxes=("Boxes_Shipped", "sum"))
        .reset_index()
    )
    mensal["Mes"] = mensal["Order_Date"].astype(str)
    # Desconto_Pct pode vir como 0-1 ou 0-100 dependendo do CSV
    desc_vals = mensal["Desconto_Medio"]
    desc_pct = desc_vals * 100 if desc_vals.mean() <= 1 else desc_vals
    fig_q3.add_trace(go.Scatter(
        x=desc_pct,
        y=mensal["Total_Boxes"],
        mode="markers",
        name=canal,
        customdata=mensal[["Mes"]].values,
        hovertemplate="<b>%{customdata[0]}</b><br>Desconto médio: %{x:.1f}%<br>Caixas: %{y:,}<extra></extra>",
        marker=dict(color=cor, size=10, opacity=0.75,
                    line=dict(color=CORES["fundo"], width=1)),
    ))

fig_q3 = estilizar(fig_q3, "")
fig_q3.update_layout(
    height=340,
    xaxis_title="Desconto Médio Mensal (%)",
    yaxis_title="Total de Caixas Enviadas",
    xaxis_ticksuffix="%",
)
st.plotly_chart(fig_q3, use_container_width=True)

insight_box(
    "Cada ponto representa um mês analisado. A nuvem não revela correlação clara entre desconto e volume — "
    "os pontos estão distribuídos de forma praticamente aleatória. Ainda assim, é possível notar que descontos "
    "exercem algum efeito no <strong>nível de vendas</strong>: no Varejo e no Atacado, estabelecimentos se beneficiam "
    "de descontos para captar consumidores de passagem, independentemente do percentual aplicado. "
    "Isso indica que é possível <strong>reduzir descontos sem sacrificar volume</strong>, "
    "melhorando a margem sem machucar a base consumidora."
)


# ─────────────────────────────────────────────
# SEÇÃO 2 · MARKETING E ROI
# ─────────────────────────────────────────────
st.markdown('<div class="ornament">· · ·</div>', unsafe_allow_html=True)
st.markdown("## Eficiência de Marketing e ROI")

# Q4 — ROI por canal (scatter marketing × receita)
st.markdown("### Q4 · Marketing Spend vs. Faturamento por Canal")

fig_q4 = go.Figure()
for canal, df_c, cor in [
    ("Varejo",  dados_varejo,  CORES["vermelho"]),
    ("Online",  dados_online,  CORES["caramelo"]),
    ("Atacado", dados_atacado, CORES["borgonha"]),
]:
    df_c2 = df_c.copy()
    df_c2["Order_Date"] = pd.to_datetime(df_c2["Order_Date"])
    mensal = (
        df_c2.groupby(df_c2["Order_Date"].dt.to_period("M"))
        .agg(Total_Marketing=("Marketing_Spend", "sum"), Total_Amount=("Amount", "sum"))
        .reset_index()
    )
    fig_q4.add_trace(go.Scatter(
        x=mensal["Total_Marketing"],
        y=mensal["Total_Amount"],
        mode="markers",
        name=canal,
        marker=dict(color=cor, size=11, opacity=0.8,
                    line=dict(color=CORES["fundo"], width=1)),
    ))

fig_q4 = estilizar(fig_q4)
fig_q4.update_layout(
    height=340,
    xaxis_title="Investimento em Marketing (R$)",
    yaxis_title="Faturamento (R$)",
    xaxis_tickprefix="R$ ",
    yaxis_tickprefix="R$ ",
)
st.plotly_chart(fig_q4, use_container_width=True)

insight_box(
    "Todos os canais apresentam crescimento proporcional do faturamento com o investimento em marketing. "
    "O canal <strong>Online</strong> se destaca com retornos milionários sobre campanhas, "
    "enquanto o Varejo e Atacado se beneficiam mais de vendas passivas por tráfego em loja."
)

# Q5 — Marketing vs Boxes ao longo do tempo
st.markdown("### Q5 · Sazonalidade: Marketing vs. Volume ao Longo do Tempo")

canal_sel = st.selectbox("Selecionar canal", ["Varejo", "Online", "Atacado"], index=0,
                          label_visibility="collapsed")
df_sel = {"Varejo": dados_varejo, "Online": dados_online, "Atacado": dados_atacado}[canal_sel]
cor_sel = CORES[{"Varejo": "vermelho", "Online": "caramelo", "Atacado": "borgonha"}[canal_sel]]

df_sel2 = df_sel.copy()
df_sel2["Order_Date"] = pd.to_datetime(df_sel2["Order_Date"])
mensal_sel = (
    df_sel2.groupby(df_sel2["Order_Date"].dt.to_period("M"))
    .agg(Total_Marketing=("Marketing_Spend", "sum"), Total_Boxes=("Boxes_Shipped", "sum"))
    .reset_index()
)
mensal_sel["Mes"] = mensal_sel["Order_Date"].astype(str)

fig_q5 = make_subplots(specs=[[{"secondary_y": True}]])
fig_q5.add_trace(go.Scatter(
    x=mensal_sel["Mes"], y=mensal_sel["Total_Marketing"],
    name="Marketing Spend",
    line=dict(color=cor_sel, width=2.5),
    mode="lines+markers",
    marker=dict(size=6),
), secondary_y=False)
fig_q5.add_trace(go.Scatter(
    x=mensal_sel["Mes"], y=mensal_sel["Total_Boxes"],
    name="Caixas Enviadas",
    line=dict(color=CORES["ouro_queimado"], width=2, dash="dot"),
    mode="lines+markers",
    marker=dict(size=6, symbol="square"),
), secondary_y=True)

fig_q5.update_layout(
    **LAYOUT_BASE,
    height=340,
    xaxis=dict(
        tickangle=-35,
        gridcolor="rgba(0,0,0,0)",
        linecolor="rgba(107,26,26,0.27)",
        tickfont=dict(color=CORES["texto_muted"], size=9),
    ),
)
fig_q5.update_yaxes(
    gridcolor="rgba(107,26,26,0.13)",
    linecolor="rgba(0,0,0,0)",
    tickfont=dict(color=CORES["texto_muted"]),
    secondary_y=False,
    tickprefix="R$ ",
)
fig_q5.update_yaxes(
    gridcolor="rgba(0,0,0,0)",
    linecolor="rgba(0,0,0,0)",
    tickfont=dict(color=CORES["ouro_queimado"]),
    secondary_y=True,
)
st.plotly_chart(fig_q5, use_container_width=True)

insight_box(
    "Não foram observados grandes picos de volume imediatamente após investimentos de marketing. "
    "Isso sugere uma base consolidada com demanda regular — o marketing atua mais como "
    "<strong>sustentação de marca</strong> do que como gerador de picos agudos."
)

# Q6 — ROI por produto (ranking)
st.markdown("### Q6 · ROI por Produto — Ranking de Eficiência")

canal_roi = st.selectbox("Canal", ["Varejo", "Online", "Atacado"], index=0,
                          key="roi_canal", label_visibility="collapsed")
df_roi_base = {"Varejo": dados_varejo, "Online": dados_online, "Atacado": dados_atacado}[canal_roi]

df_roi_prod = (
    df_roi_base.groupby("Product")
    .agg(Receita=("Amount", "sum"), Marketing=("Marketing_Spend", "sum"))
    .reset_index()
)
df_roi_prod = df_roi_prod[df_roi_prod["Marketing"] > 0].copy()
df_roi_prod["ROI"] = df_roi_prod["Receita"] / df_roi_prod["Marketing"]
df_roi_prod = df_roi_prod.sort_values("ROI").tail(9)

cor_roi = CORES[{"Varejo": "vermelho", "Online": "caramelo", "Atacado": "borgonha"}[canal_roi]]
n = len(df_roi_prod)
escala = [
    f"rgba({int(c[1:3],16)},{int(c[2:4],16) if len(c)==7 else 0},{int(c[5:7],16) if len(c)==7 else 0},{0.45 + 0.55*i/max(n-1,1):.2f})"
    for i, c in enumerate([cor_roi]*n)
]

fig_q6 = go.Figure(go.Bar(
    x=df_roi_prod["ROI"],
    y=df_roi_prod["Product"],
    orientation="h",
    marker=dict(
        color=df_roi_prod["ROI"].values,
        colorscale=[
            [0,   CORES["borgonha"]],
            [0.5, CORES["vermelho"]],
            [1,   CORES["vermelho_vivo"]],
        ],
        showscale=False,
    ),
    text=[f"{v:.1f}×" for v in df_roi_prod["ROI"]],
    textposition="outside",
    textfont=dict(color=CORES["texto"], size=11),
))
fig_q6 = estilizar(fig_q6)
fig_q6.update_layout(
    height=360,
    xaxis_title="Receita por R$ 1 investido em Marketing",
    yaxis=dict(
        gridcolor="rgba(0,0,0,0)",
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(color=CORES["texto_muted"], size=10),
    ),
)
st.plotly_chart(fig_q6, use_container_width=True)

insight_box(
    "As <strong>caixas sortidas</strong> (Mixed Assortment) apresentam ROI acima de 10× nos três canais. "
    "O fator surpresa e a diversidade de produtos parecem ser altamente valorizados pelo consumidor, "
    "tornando esse formato um campeão de eficiência de marketing."
)


# ─────────────────────────────────────────────
# SEÇÃO 3 · SAZONALIDADE
# ─────────────────────────────────────────────
st.markdown('<div class="ornament">· · ·</div>', unsafe_allow_html=True)
st.markdown("## Sazonalidade e Tendências Temporais")

# Q7 — Faturamento mensal por canal
st.markdown("### Q7 · Faturamento Mensal — Picos Sazonais")

fig_q7 = go.Figure()
for canal, df_c, cor in [
    ("Varejo",  dados_varejo,  CORES["vermelho"]),
    ("Online",  dados_online,  CORES["caramelo"]),
    ("Atacado", dados_atacado, CORES["borgonha"]),
]:
    df_c2 = df_c.copy()
    df_c2["Order_Date"] = pd.to_datetime(df_c2["Order_Date"])
    mensal = (
        df_c2.groupby(df_c2["Order_Date"].dt.to_period("M"))
        .agg(Total_Amount=("Amount", "sum"))
        .reset_index()
    )
    mensal["Mes"] = mensal["Order_Date"].astype(str)
    fig_q7.add_trace(go.Scatter(
        x=mensal["Mes"], y=mensal["Total_Amount"],
        name=canal,
        line=dict(color=cor, width=2.5),
        mode="lines+markers",
        marker=dict(size=5),
    ))

# Anotações de picos
fig_q7.add_vrect(x0="2022-03", x1="2022-05", fillcolor=CORES["caramelo"],
                  opacity=0.07, layer="below", line_width=0, annotation_text="Páscoa '22",
                  annotation_position="top left", annotation_font_color=CORES["ouro_queimado"],
                  annotation_font_size=10)
fig_q7.add_vrect(x0="2022-11", x1="2023-01", fillcolor=CORES["vermelho"],
                  opacity=0.07, layer="below", line_width=0, annotation_text="Natal '22",
                  annotation_position="top left", annotation_font_color=CORES["caramelo"],
                  annotation_font_size=10)
fig_q7.add_vrect(x0="2023-03", x1="2023-05", fillcolor=CORES["caramelo"],
                  opacity=0.07, layer="below", line_width=0)
fig_q7.add_vrect(x0="2023-11", x1="2023-12", fillcolor=CORES["vermelho"],
                  opacity=0.07, layer="below", line_width=0)

fig_q7 = estilizar(fig_q7)
fig_q7.update_layout(
    height=370,
    xaxis=dict(
        tickangle=-35,
        gridcolor="rgba(0,0,0,0)",
        linecolor="rgba(107,26,26,0.27)",
        tickfont=dict(color=CORES["texto_muted"], size=9),
    ),
    yaxis_tickprefix="R$ ",
)
st.plotly_chart(fig_q7, use_container_width=True)

insight_box(
    "Picos históricos de faturamento ocorrem no <strong>Fim de Ano (novembro–dezembro)</strong> em todos os canais. "
    "A <strong>Páscoa (março–abril)</strong> gera picos locais secundários — "
    "sazonalidades esperadas para produtos de chocolate."
)

# Q8 — Tendência online vs físicos
st.markdown("### Q8 · Crescimento Online vs. Canais Físicos")

fig_q8 = go.Figure()
for canal, df_c, cor, dash in [
    ("Varejo",  dados_varejo,  CORES["vermelho"],  "solid"),
    ("Online",  dados_online,  CORES["caramelo"],  "solid"),
    ("Atacado", dados_atacado, CORES["borgonha"],  "solid"),
]:
    df_c2 = df_c.copy()
    df_c2["Order_Date"] = pd.to_datetime(df_c2["Order_Date"])
    mensal = (
        df_c2.groupby(df_c2["Order_Date"].dt.to_period("M"))
        .agg(Total_Boxes=("Boxes_Shipped", "sum"))
        .reset_index()
    )
    mensal["Mes"] = mensal["Order_Date"].astype(str)
    fig_q8.add_trace(go.Scatter(
        x=mensal["Mes"], y=mensal["Total_Boxes"],
        name=canal,
        line=dict(color=cor, width=2.5, dash=dash),
        mode="lines",
        fill="tozeroy" if canal == "Online" else None,
        fillcolor="rgba(139,69,19,0.09)" if canal == "Online" else None,
    ))

fig_q8 = estilizar(fig_q8)
fig_q8.update_layout(
    height=340,
    xaxis=dict(
        tickangle=-35,
        gridcolor="rgba(0,0,0,0)",
        linecolor="rgba(107,26,26,0.27)",
        tickfont=dict(color=CORES["texto_muted"], size=9),
    ),
    yaxis_title="Caixas Enviadas",
)
st.plotly_chart(fig_q8, use_container_width=True)

insight_box(
    "Os faturamentos permanecem <strong>estáveis</strong> nos três canais ao longo do período, "
    "sem crescimento explosivo do Online sobre os físicos. Isso reflete uma base de clientes consolidada "
    "com demanda regular — o que favorece previsibilidade, mas indica oportunidade latente "
    "para expansão da base consumidora digital."
)


# ─────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────
st.markdown('<div class="ornament">· · ·</div>', unsafe_allow_html=True)
st.markdown(f"""
<p style="text-align:center;font-size:0.78rem;color:{CORES['borgonha']};letter-spacing:0.08em;">
  Análise Exploratória · Chocolateria Brasil · 2022–2023
</p>
""", unsafe_allow_html=True)
