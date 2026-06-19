import os
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "etl"))
from questionnaire_map import BLOCK_MAP  # noqa: E402

DATA_PATH = os.path.join(ROOT, "data", "fact_long.csv")

COLORS = {
    "Sim": "#2E7D32",
    "Parcialmente": "#F9A825",
    "Não": "#C62828",
    "Não Informado": "#BDBDBD",
}
RESP_ORDER = ["Sim", "Parcialmente", "Não", "Não Informado"]
MULTI_CHOICE_IDS = {"C12_Tipo", "F04_Tipo"}

# Padrão aplicado a todos os gráficos Plotly: fundo branco + texto escuro
_CHART_DEFAULTS = dict(
    paper_bgcolor="rgba(255,255,255,1)",
    plot_bgcolor="rgba(255,255,255,1)",
    font=dict(color="#1a1a1a"),
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fiscalização de Creches 2026",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Fundo azul em todas as camadas do Streamlit */
    .stApp,
    .stApp > div,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > div,
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    .main,
    .block-container {
        background-color: #74B2E2 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background-color: #1a559a !important;
        border-right: 1px solid #154888;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown { color: #e8f0ff !important; }

    /* Divisores e tabs */
    hr { border-color: rgba(255,255,255,0.3) !important; }
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] button { color: #ffffff !important; }

    /* Labels dos filtros */
    .stMultiSelect label,
    .stSelectbox label,
    .stTextInput label { color: #ffffff !important; }

    /* Caption */
    [data-testid="stCaptionContainer"] p { color: #dceeff !important; }

    /* Cards dos gráficos */
    div[data-testid="stPlotlyChart"] {
        background: #ffffff !important;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        padding: 4px;
        overflow: hidden;
    }

    /* Card da tabela */
    div[data-testid="stDataFrame"] {
        background: #ffffff !important;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        overflow: hidden;
    }

    /* Input de busca */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border-color: #cccccc !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Helpers de UI ─────────────────────────────────────────────────────────────
def _h2(text: str) -> None:
    st.markdown(
        f"<p style='color:#ffffff;font-size:1.7rem;font-weight:700;"
        f"margin:8px 0 12px 0;line-height:1.2'>{text}</p>",
        unsafe_allow_html=True,
    )


def _h4(text: str) -> None:
    st.markdown(
        f"<p style='color:#ffffff;font-size:1.1rem;font-weight:600;"
        f"margin:10px 0 4px 0'>{text}</p>",
        unsafe_allow_html=True,
    )


def _metric_card(label: str, value, border_color: str = "#2E7D32") -> str:
    return f"""
    <div style="background:#ffffff;border-radius:10px;padding:14px 18px;
                border-left:4px solid {border_color};
                box-shadow:0 2px 10px rgba(0,0,0,0.15);margin-bottom:8px;">
        <p style="margin:0;font-size:0.75rem;color:#666666;font-weight:600;
                  text-transform:uppercase;letter-spacing:0.05em">{label}</p>
        <p style="margin:4px 0 0 0;font-size:1.5rem;font-weight:700;color:#1a1a1a;">{value}</p>
    </div>
    """


# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    if not os.path.exists(DATA_PATH):
        st.error("Execute primeiro: `python etl/etl.py`")
        st.stop()
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    valid = {"Sim", "Não", "Parcialmente"}
    df["Resposta_Chart"] = df["Resposta"].apply(
        lambda r: r if r in valid else "Não Informado"
    )
    return df


df_all = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Fiscalização de Creches 2026")
    st.caption("TCE-MT · Infraestrutura e Fila de Espera")
    st.divider()

    municipios = ["Todos"] + sorted(df_all["Qmun"].dropna().unique())
    sel_mun = st.selectbox("Município", municipios)

    if sel_mun == "Todos":
        uni_pool = df_all
    else:
        uni_pool = df_all[df_all["Qmun"] == sel_mun]

    unidades = ["Todas"] + sorted(uni_pool["Qnome_unidade"].dropna().unique())
    sel_uni = st.selectbox("Unidade / Creche", unidades)

    st.divider()
    st.caption("Respostas válidas: Sim · Não · Parcialmente")

# ── Filtro ────────────────────────────────────────────────────────────────────
df = df_all.copy()
if sel_mun != "Todos":
    df = df[df["Qmun"] == sel_mun]
if sel_uni != "Todas":
    df = df[df["Qnome_unidade"] == sel_uni]

df_units = (
    df[["Qmun", "Qnome_unidade", "Qcount_criancas_num"]]
    .drop_duplicates(subset=["Qmun", "Qnome_unidade"])
)
df_valid = df[df["Resposta_Valida"]]

# ── Métricas base ─────────────────────────────────────────────────────────────
n_municipios = df_units["Qmun"].nunique()
n_unidades   = df_units["Qnome_unidade"].nunique()
n_criancas   = int(df_units["Qcount_criancas_num"].sum())
conf_geral   = round((df_valid["Resposta"] == "Sim").sum() / max(len(df_valid), 1) * 100, 1)

df_g_valid = df[(df["Bloco_ID"] == "G") & df["Resposta_Valida"]]
inconf_g   = round((df_g_valid["Resposta"] == "Não").sum() / max(len(df_g_valid), 1) * 100, 1)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "Main Page",
    "Segmentos por Bloco",
    "Indicadores por Pergunta",
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 – MAIN PAGE
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    _h2("Painel Geral")

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(_metric_card("Municípios", n_municipios), unsafe_allow_html=True)
    with k2:
        st.markdown(_metric_card("Unidades fiscalizadas", n_unidades), unsafe_allow_html=True)
    with k3:
        st.markdown(
            _metric_card("Crianças atendidas", f"{n_criancas:,}".replace(",", ".")),
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(_metric_card("Conformidade geral", f"{conf_geral}%", "#1565C0"), unsafe_allow_html=True)
    with k5:
        st.markdown(_metric_card("Inconformidade Bloco G", f"{inconf_g}%", "#C62828"), unsafe_allow_html=True)

    st.divider()

    # Calcula altura garantindo que o gráfico de creches tenha espaço suficiente
    n_mun     = len(df_units["Qmun"].unique())
    donut_h   = 260
    creches_h = max(350, n_mun * 22)
    CHART_H   = max(donut_h + creches_h + 80, n_mun * 28)

    col_bar, col_donut = st.columns([3, 2])

    with col_bar:
        _h4("Municípios por Crianças Atendidas")
        mun_cri = (
            df_units.groupby("Qmun")["Qcount_criancas_num"]
            .sum().reset_index()
            .sort_values("Qcount_criancas_num", ascending=True)
        )
        fig_bar = px.bar(
            mun_cri, x="Qcount_criancas_num", y="Qmun", orientation="h",
            labels={"Qcount_criancas_num": "Crianças", "Qmun": ""},
            color="Qcount_criancas_num",
            color_continuous_scale=["#a5d6a7", "#1B5E20"],
            text="Qcount_criancas_num",
        )
        fig_bar.update_traces(
            textposition="outside",
            textfont=dict(color="#1a1a1a"),
            cliponaxis=False,
        )
        fig_bar.update_layout(
            coloraxis_showscale=False,
            margin=dict(l=0, r=60, t=10, b=10),
            height=CHART_H,
            **_CHART_DEFAULTS,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_donut:

        _h4("Distribuição Geral das Respostas")
        st.caption("Apenas respostas categóricas (exclui campos de múltipla escolha)")
        df_donut = df[~df["ID_Pergunta"].isin(MULTI_CHOICE_IDS)]
        dist = (
            df_donut.groupby("Resposta_Chart").size()
            .reindex(RESP_ORDER, fill_value=0)
            .reset_index(name="Qtd")
            .rename(columns={"Resposta_Chart": "Resposta"})
        )
        dist = dist[dist["Qtd"] > 0]
        fig_donut = go.Figure(go.Pie(
            labels=dist["Resposta"],
            values=dist["Qtd"],
            hole=0.55,
            marker_colors=[COLORS[r] for r in dist["Resposta"]],
            textinfo="label+percent",
            textfont=dict(color="#ffffff"),
            sort=False,
        ))
        fig_donut.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=-0.05, x=0.5, xanchor="center"),
            height=donut_h,
            **_CHART_DEFAULTS,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

        _h4("Creches Visitadas por Município")
        creches_mun = (
            df_units.groupby("Qmun")["Qnome_unidade"]
            .count().reset_index()
            .rename(columns={"Qnome_unidade": "Creches"})
            .sort_values("Creches", ascending=True)
        )
        fig_creches = px.bar(
            creches_mun, x="Creches", y="Qmun", orientation="h",
            labels={"Qmun": "", "Creches": "Unidades"},
            color="Creches",
            color_continuous_scale=["#bbdefb", "#1565C0"],
            text="Creches",
        )
        fig_creches.update_traces(
            textposition="outside",
            textfont=dict(color="#1a1a1a"),
            cliponaxis=False,
        )
        fig_creches.update_layout(
            coloraxis_showscale=False,
            margin=dict(l=0, r=60, t=10, b=10),
            height=creches_h,
            **_CHART_DEFAULTS,
        )
        st.plotly_chart(fig_creches, use_container_width=True)

    st.divider()

    _h4("Distribuição das Respostas de Múltipla Escolha")

    def dist_multi(col_id: str):
        subset = (
            df[df["ID_Pergunta"] == col_id]
            .drop_duplicates(subset=["Qnome_unidade"])
        )
        n_total = len(subset)
        items = (
            subset["Resposta"]
            .str.split(r"\s*\|\s*")
            .explode()
            .str.strip()
        )
        counts = items.value_counts().reset_index()
        counts.columns = ["Item", "Qtd"]
        counts["% Unidades"] = (counts["Qtd"] / n_total * 100).round(1)
        return counts, n_total

    col_c12, col_f04 = st.columns(2)

    with col_c12:
        st.markdown("<b style='color:white'>Acessibilidade Física (C12)</b>", unsafe_allow_html=True)
        c12_data, c12_total = dist_multi("C12_Tipo")
        fig_c12 = px.bar(
            c12_data.sort_values("% Unidades", ascending=True),
            x="% Unidades", y="Item", orientation="h",
            text="% Unidades",
            color="% Unidades",
            color_continuous_scale=["#a5d6a7", "#1B5E20"],
            labels={"Item": "", "% Unidades": "% das unidades"},
        )
        fig_c12.update_traces(texttemplate="%{text}%", textposition="outside", textfont=dict(color="#1a1a1a"), cliponaxis=False)
        fig_c12.update_layout(
            coloraxis_showscale=False,
            xaxis_range=[0, 120],
            margin=dict(l=0, r=40, t=10, b=10),
            height=260,
            **_CHART_DEFAULTS,
        )
        st.caption(f"Base: {c12_total} unidades")
        st.plotly_chart(fig_c12, use_container_width=True)

    with col_f04:
        st.markdown("<b style='color:white'>Formas de Comunicação com as Famílias (F04)</b>", unsafe_allow_html=True)
        f04_data, f04_total = dist_multi("F04_Tipo")
        fig_f04 = px.bar(
            f04_data.sort_values("% Unidades", ascending=True),
            x="% Unidades", y="Item", orientation="h",
            text="% Unidades",
            color="% Unidades",
            color_continuous_scale=["#bbdefb", "#1565C0"],
            labels={"Item": "", "% Unidades": "% das unidades"},
        )
        fig_f04.update_traces(texttemplate="%{text}%", textposition="outside", textfont=dict(color="#1a1a1a"), cliponaxis=False)
        fig_f04.update_layout(
            coloraxis_showscale=False,
            xaxis_range=[0, 120],
            margin=dict(l=0, r=40, t=10, b=10),
            height=260,
            **_CHART_DEFAULTS,
        )
        st.caption(f"Base: {f04_total} unidades")
        st.plotly_chart(fig_f04, use_container_width=True)

    st.divider()

    _h4("Conformidade por Município (%)")
    conf_mun = (
        df[df["Resposta_Valida"]]
        .groupby("Qmun")["Resposta"]
        .apply(lambda x: round((x == "Sim").sum() / len(x) * 100, 1))
        .reset_index().rename(columns={"Resposta": "Conformidade (%)"})
        .sort_values("Conformidade (%)", ascending=False)
    )
    fig_conf = px.bar(
        conf_mun, x="Qmun", y="Conformidade (%)",
        color="Conformidade (%)",
        color_continuous_scale=["#C62828", "#F9A825", "#2E7D32"],
        range_color=[0, 100],
        text="Conformidade (%)",
        labels={"Qmun": ""},
    )
    fig_conf.update_traces(texttemplate="%{text}%", textposition="outside", textfont=dict(color="#1a1a1a"), cliponaxis=False)
    fig_conf.update_layout(
        coloraxis_showscale=False,
        yaxis_range=[0, 115],
        xaxis_tickangle=-35,
        xaxis=dict(automargin=True),
        margin=dict(l=10, r=10, t=10, b=100),
        height=400,
        **_CHART_DEFAULTS,
    )
    st.plotly_chart(fig_conf, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 – SEGMENTOS POR BLOCO
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    _h2("Análise por Bloco do Questionário")

    blocos_disp = sorted(df["Bloco_ID"].unique())
    sel_blocos = st.multiselect(
        "Filtrar blocos",
        options=blocos_disp,
        default=blocos_disp,
        format_func=lambda b: BLOCK_MAP.get(b, b),
    )

    df_seg = df[df["Bloco_ID"].isin(sel_blocos)]
    df_seg_valid = df_seg[df_seg["Resposta_Valida"]]

    if df_seg_valid.empty:
        st.info("Nenhum dado para os filtros selecionados.")
    else:
        col_l, col_r = st.columns(2)

        with col_l:
            _h4("Aderência por Bloco (% Sim)")
            conf_bloco = (
                df_seg_valid.groupby("Bloco_ID")["Resposta"]
                .apply(lambda x: round((x == "Sim").sum() / len(x) * 100, 1))
                .reset_index().rename(columns={"Resposta": "Conformidade (%)"})
                .sort_values("Conformidade (%)", ascending=True)
            )
            conf_bloco["Bloco"] = conf_bloco["Bloco_ID"].map(BLOCK_MAP)
            fig_cb = px.bar(
                conf_bloco, x="Conformidade (%)", y="Bloco", orientation="h",
                text="Conformidade (%)",
                color="Conformidade (%)",
                color_continuous_scale=["#C62828", "#F9A825", "#2E7D32"],
                range_color=[0, 100],
                labels={"Bloco": ""},
            )
            fig_cb.update_traces(texttemplate="%{text}%", textposition="outside", textfont=dict(color="#1a1a1a"), cliponaxis=False)
            fig_cb.update_layout(
                coloraxis_showscale=False,
                xaxis_range=[0, 115],
                yaxis=dict(automargin=True),
                margin=dict(l=10, r=30, t=10, b=10),
                height=320,
                **_CHART_DEFAULTS,
            )
            st.plotly_chart(fig_cb, use_container_width=True)

        with col_r:
            _h4("Pontos de Atenção por Bloco (% Não)")
            inconf_bloco = (
                df_seg_valid.groupby("Bloco_ID")["Resposta"]
                .apply(lambda x: round((x == "Não").sum() / len(x) * 100, 1))
                .reset_index().rename(columns={"Resposta": "Inconformidade (%)"})
                .sort_values("Inconformidade (%)", ascending=True)
            )
            inconf_bloco["Bloco"] = inconf_bloco["Bloco_ID"].map(BLOCK_MAP)
            fig_ib = px.bar(
                inconf_bloco, x="Inconformidade (%)", y="Bloco", orientation="h",
                text="Inconformidade (%)",
                color="Inconformidade (%)",
                color_continuous_scale=["#FFCDD2", "#C62828"],
                labels={"Bloco": ""},
            )
            fig_ib.update_traces(texttemplate="%{text}%", textposition="outside", textfont=dict(color="#1a1a1a"), cliponaxis=False)
            fig_ib.update_layout(
                coloraxis_showscale=False,
                xaxis_range=[0, 115],
                yaxis=dict(automargin=True),
                margin=dict(l=10, r=30, t=10, b=10),
                height=320,
                **_CHART_DEFAULTS,
            )
            st.plotly_chart(fig_ib, use_container_width=True)

        st.divider()

        _h4("Distribuição de Respostas por Bloco")
        resp_bloco = (
            df_seg.groupby(["Bloco_ID", "Resposta_Chart"])
            .size().reset_index(name="Qtd")
        )
        resp_bloco["Bloco"] = resp_bloco["Bloco_ID"].map(BLOCK_MAP)
        fig_stack = px.bar(
            resp_bloco, x="Bloco", y="Qtd",
            color="Resposta_Chart",
            color_discrete_map=COLORS,
            category_orders={"Resposta_Chart": RESP_ORDER},
            barmode="stack",
            labels={"Bloco": "", "Qtd": "Respostas", "Resposta_Chart": "Resposta"},
        )
        fig_stack.update_layout(
            margin=dict(l=10, r=160, t=10, b=80),
            height=380,
            xaxis_tickangle=-25,
            legend=dict(
                orientation="v",
                x=1.02, xanchor="left",
                y=0.5, yanchor="middle",
                title="",
            ),
            **_CHART_DEFAULTS,
        )
        st.plotly_chart(fig_stack, use_container_width=True)

        st.divider()

        _h4("Top 10 Perguntas com Maior Índice de Inconformidade")
        top_nao = (
            df_seg_valid.groupby(["ID_Pergunta", "Texto_Pergunta"])["Resposta"]
            .apply(lambda x: round((x == "Não").sum() / len(x) * 100, 1))
            .reset_index().rename(columns={"Resposta": "% Não"})
            .sort_values("% Não", ascending=False).head(10)
        )
        top_nao["Label"] = (
            top_nao["ID_Pergunta"] + " – "
            + top_nao["Texto_Pergunta"].str[:70] + "…"
        )
        fig_top = px.bar(
            top_nao, x="% Não", y="Label", orientation="h",
            text="% Não",
            color="% Não",
            color_continuous_scale=["#FFCDD2", "#C62828"],
            labels={"Label": ""},
        )
        fig_top.update_traces(texttemplate="%{text}%", textposition="outside", textfont=dict(color="#1a1a1a"), cliponaxis=False)
        fig_top.update_layout(
            coloraxis_showscale=False,
            xaxis_range=[0, 115],
            margin=dict(l=10, r=30, t=10, b=10),
            height=420,
            yaxis={"autorange": "reversed", "automargin": True},
            **_CHART_DEFAULTS,
        )
        st.plotly_chart(fig_top, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 – INDICADORES POR PERGUNTA
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    _h2("Indicadores por Pergunta")

    perguntas_df = (
        df[["ID_Pergunta", "Texto_Pergunta", "Bloco_ID"]]
        .drop_duplicates(subset=["ID_Pergunta"])
        .sort_values(["Bloco_ID", "ID_Pergunta"])
    )
    opcoes = {
        row["ID_Pergunta"]: (
            f"[{BLOCK_MAP.get(row['Bloco_ID'], row['Bloco_ID'])}]  "
            f"{row['ID_Pergunta']} – {row['Texto_Pergunta']}"
        )
        for _, row in perguntas_df.iterrows()
    }

    pergunta_sel = st.selectbox(
        "Pergunta", options=list(opcoes.keys()),
        format_func=lambda k: opcoes[k],
    )

    df_perg       = df[df["ID_Pergunta"] == pergunta_sel]
    df_perg_valid = df_perg[df_perg["Resposta_Valida"]]

    if not df_perg.empty:
        st.markdown(
            f"<p style='color:#ffffff;font-size:1rem;font-style:italic;margin:4px 0 8px 0'>"
            f"<b>{df_perg['Texto_Pergunta'].iloc[0]}</b></p>",
            unsafe_allow_html=True,
        )

    st.divider()

    n_sim  = int((df_perg["Resposta"] == "Sim").sum())
    n_nao  = int((df_perg["Resposta"] == "Não").sum())
    n_parc = int((df_perg["Resposta"] == "Parcialmente").sum())
    n_ni   = int((~df_perg["Resposta_Valida"]).sum())
    conf_p = round(n_sim / max(len(df_perg_valid), 1) * 100, 1)

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(_metric_card("Sim", n_sim, "#2E7D32"), unsafe_allow_html=True)
    with m2:
        st.markdown(_metric_card("Não", n_nao, "#C62828"), unsafe_allow_html=True)
    with m3:
        st.markdown(_metric_card("Parcialmente", n_parc, "#F9A825"), unsafe_allow_html=True)
    with m4:
        st.markdown(_metric_card("Não Informado", n_ni, "#9E9E9E"), unsafe_allow_html=True)
    with m5:
        st.markdown(_metric_card("Conformidade", f"{conf_p}%", "#1565C0"), unsafe_allow_html=True)

    dist_p = (
        df_perg.groupby("Resposta_Chart").size()
        .reindex(RESP_ORDER, fill_value=0)
        .reset_index(name="Qtd")
        .rename(columns={"Resposta_Chart": "Resposta"})
    )
    dist_p = dist_p[dist_p["Qtd"] > 0]
    fig_mini = go.Figure(go.Pie(
        labels=dist_p["Resposta"], values=dist_p["Qtd"],
        hole=0.6,
        marker_colors=[COLORS[r] for r in dist_p["Resposta"]],
        textinfo="label+percent",
        textfont=dict(color="#ffffff"),
        sort=False,
    ))
    fig_mini.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        showlegend=True,
        legend=dict(orientation="h", yanchor="top", y=-0.05, x=0.5, xanchor="center"),
        **_CHART_DEFAULTS,
    )
    _, col_mini, _ = st.columns([1, 2, 1])
    with col_mini:
        st.plotly_chart(fig_mini, use_container_width=True)

    st.divider()
    _h4("Detalhamento por Unidade")

    busca = st.text_input("Buscar unidade ou município", placeholder="Digite para filtrar…")

    tabela = (
        df_perg[["Qmun", "Qnome_unidade", "Resposta"]]
        .rename(columns={"Qmun": "Município", "Qnome_unidade": "Unidade"})
        .sort_values(["Município", "Unidade"])
        .reset_index(drop=True)
    )

    if busca:
        mask_b = (
            tabela["Município"].str.contains(busca, case=False, na=False)
            | tabela["Unidade"].str.contains(busca, case=False, na=False)
        )
        tabela = tabela[mask_b].reset_index(drop=True)

    def _style_row(row):
        r = row["Resposta"]
        base = ["", ""]
        if r == "Não":
            return base + ["background-color:#FFCDD2;color:#B71C1C;font-weight:bold"]
        if r == "Parcialmente":
            return base + ["background-color:#FFF9C4;color:#7B6000"]
        if r == "Sim":
            return base + ["background-color:#C8E6C9;color:#1B5E20"]
        return base + ["color:#9E9E9E"]

    st.dataframe(
        tabela.style.apply(_style_row, axis=1),
        use_container_width=True,
        height=500,
    )
