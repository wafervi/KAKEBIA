import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# 1. Configuración general de la página
st.set_page_config(
    page_title="ANÁLISIS DE GASTOS - KAKEBIA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inyección de CSS personalizado para emular la tarjeta y diseño del dashboard
st.markdown("""
    <style>
    /* Fondo general del dashboard */
    .stApp {
        background-color: #161b2e;
        color: #f8fafc;
    }
    [data-testid="stAppViewContainer"] {
        background: #161b2e;
    }
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    [data-testid="stSidebar"] {
        background: #111629;
        border-right: 1px solid #2b3452;
    }
    [data-testid="stSidebar"] * {
        color: #dbe4ff;
    }
    [data-testid="stMultiSelect"] > div > div {
        background: #202742;
        border-color: #3b466a;
    }
    
    /* Encabezado Principal */
    .main-header {
        background-color: #1d243b;
        padding: 18px 30px;
        border-radius: 6px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.25);
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #2e3859;
    }
    .main-header h1 {
        color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        font-size: 24px;
        margin: 0;
        letter-spacing: 1px;
    }

    /* Estilo de Contenedores / Tarjetas */
    .card-container {
        background-color: #1d243b;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.28);
        border: 1px solid #2e3859;
        margin-bottom: 20px;
    }
    
    .card-title {
        font-size: 14px;
        font-weight: 700;
        color: #cbd5f5;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        text-align: center;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 1px solid #34405f;
    }

    /* KPI Box */
    .kpi-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 45px 20px;
        background-color: #242d48;
        border-radius: 5px;
        border: 1px solid #34405f;
        margin-top: 10px;
    }
    .kpi-value {
        font-size: 36px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 8px;
        font-family: 'Segoe UI', sans-serif;
    }
    .kpi-subtext {
        font-size: 13px;
        color: #94a3c8;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid #34405f;
    }
    [data-testid="stDataFrame"] iframe {
        background: #1d243b;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Carga y preparación de los datos
@st.cache_data
def load_data():
    data_path = Path(__file__).resolve().parents[1] / 'data' / 'processed' / 'kakebo_pred_hist.csv'
    df = pd.read_csv(data_path)
    df['fecha_dt'] = pd.to_datetime(df['fecha'])
    df['Año'] = df['fecha_dt'].dt.year
    
    meses_es = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    df['Mes'] = df['fecha_dt'].dt.month.map(meses_es)
    return df

df = load_data()

# Header Superior
st.markdown("""
    <div class="main-header">
        <h1>🤖 ANÁLISIS DE GASTOS - KAKEBIA 🧮</h1>
    </div>
""", unsafe_allow_html=True)

# Sidebar para Filtros
st.sidebar.header("⚙️ Filtros de Selección")
tipos_sel = st.sidebar.multiselect(
    "Tipo de Dato:",
    options=df['tipo_dato'].unique(),
    default=df['tipo_dato'].unique()
)

anios_sel = st.sidebar.multiselect(
    "Año:",
    options=sorted(df['Año'].unique()),
    default=sorted(df['Año'].unique())
)

# Filtrar DataFrame según selección
df_filtered = df[(df['tipo_dato'].isin(tipos_sel)) & (df['Año'].isin(anios_sel))].copy()

# ---------------- FILA 1 ----------------
col1, col2 = st.columns([2, 3])

# Tarjeta 1: KPI Total
with col1:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">KPI - TOTAL EJECUTADO</div>', unsafe_allow_html=True)
    
    total_monto = df_filtered['monto'].sum()
    formatted_total = f"$ {total_monto:,.0f}".replace(",", ".")
    
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-value">{formatted_total}</div>
            <div class="kpi-subtext">MONTO EN PESOS COLOMBIANOS - (COP)</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tarjeta 2: Gráfico de Línea de Tiempo
with col2:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">GASTOS EN LÍNEA DE TIEMPO</div>', unsafe_allow_html=True)
    
    fig_line = px.line(
        df_filtered,
        x='fecha',
        y='monto',
        color='tipo_dato',
        color_discrete_map={'REAL': '#24a8ff', 'PREDICCION': '#ff9f43'},
        markers=True
    )
    fig_line.update_layout(
        xaxis_title="Año",
        yaxis_title="Monto (COP)",
        legend_title="TIPO DE DATO:",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        font=dict(color='#dbe4ff'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig_line.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#303a59', zerolinecolor='#303a59')
    fig_line.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#303a59', zerolinecolor='#303a59')
    
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FILA 2 ----------------
col3, col4 = st.columns([2, 3])

# Tarjeta 3: Tabla Consolidada
with col3:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">CONSOLIDADO DE GASTOS</div>', unsafe_allow_html=True)
    
    table_df = df_filtered[['Año', 'Mes', 'monto', 'tipo_dato']].sort_values(by='monto', ascending=True)
    table_display = table_df.copy()
    table_display['MONTO'] = table_display['monto'].apply(lambda x: f"$ {x:,.0f}".replace(",", "."))
    table_display = table_display[['Año', 'Mes', 'MONTO', 'tipo_dato']]
    table_display.columns = ['Año', 'Mes', 'MONTO', 'TIPO DE DATO']
    
    st.dataframe(
        table_display,
        use_container_width=True,
        height=280,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Tarjeta 4: Gráfico Donut de Porcentajes
with col4:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">PORCENTAJE DE MONTOS GASTADOS</div>', unsafe_allow_html=True)
    
    df_mes = df_filtered.groupby('Mes', as_index=False)['monto'].sum().sort_values(by='monto', ascending=False)
    
    fig_donut = px.pie(
        df_mes,
        values='monto',
        names='Mes',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_donut.update_traces(
        textposition='outside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#ffffff', width=2))
    )
    fig_donut.update_layout(
        legend_title="MES:",
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        font=dict(color='#dbe4ff'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)