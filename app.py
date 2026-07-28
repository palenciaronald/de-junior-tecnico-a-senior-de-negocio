"""Recomendación diaria de liquidez — Dashboard Streamlit.

Uso:
    streamlit run app.py
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent

# --- Config ---
st.set_page_config(page_title="Recomendación de Liquidez", layout="wide")
st.title("💰 Recomendación diaria de liquidez")
st.caption("Producto de datos — Billetera digital ficticia")

# --- Load data ---
@st.cache_data
def load_data():
    raw = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "daily_withdrawals.csv", parse_dates=["date"])
    test = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "test.csv", parse_dates=["date"])
    rec = pd.read_csv(PROJECT_ROOT / "outputs" / "daily_recommendation.csv", parse_dates=["date"])
    backtest = pd.read_csv(PROJECT_ROOT / "outputs" / "business_backtest.csv", parse_dates=["date"])

    metadata_path = PROJECT_ROOT / "artifacts" / "model_metadata.json"
    if metadata_path.exists():
        metadata = json.load(open(metadata_path))
    else:
        metadata = {"version": "1.0.0", "trained_at": "N/A"}

    return raw, test, rec, backtest, metadata

raw_df, test_df, rec_df, backtest_df, model_meta = load_data()

# --- Sidebar: Simulador ---
st.sidebar.header("⚙️ Simulador de parámetros")
cost_idle = st.sidebar.slider(
    "Costo ociosidad (%/día)", 0.005, 0.050, 0.010, 0.001, format="%.3f"
) / 100
cost_shortage = st.sidebar.slider(
    "Costo faltante (%/día)", 0.010, 0.200, 0.050, 0.005, format="%.3f"
) / 100
service_level = st.sidebar.slider(
    "Nivel de servicio (%)", 80, 99, 95, 1
) / 100

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Modelo:** v{model_meta.get('version', '1.0.0')}")
st.sidebar.markdown(f"**Actualización:** {model_meta.get('trained_at', 'N/A')[:10]}")

# --- Recalculate with slider params ---
reserved = rec_df["recommended_amount"].values
actual = test_df["total_withdrawals_cop"].values[:len(reserved)]

idle = np.maximum(reserved - actual, 0)
shortage = np.maximum(actual - reserved, 0)
cost_total = cost_idle * idle + cost_shortage * shortage
achieved_service = np.mean(reserved >= actual) * 100

# --- KPI Cards ---
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Monto recomendado", f"{rec_df['recommended_amount'].iloc[-1]/1e9:.1f}B")
col2.metric("Pronóstico central", f"{rec_df['forecast_central'].iloc[-1]/1e9:.1f}B")
col3.metric("Buffer", f"{rec_df['buffer'].iloc[-1]/1e9:.1f}B")
col4.metric("Nivel de servicio", f"{achieved_service:.1f}%")
col5.metric("Costo total periodo", f"{cost_total.sum()/1e6:.1f}M")

st.markdown("---")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📈 Histórico", "🔮 Pronóstico", "📊 Decisión"])

with tab1:
    fig = px.line(raw_df, x="date", y="total_withdrawals_cop",
                  title="Retiros diarios históricos (COP)")
    fig.update_layout(yaxis_title="COP", xaxis_title="", height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=test_df["date"][:len(reserved)], y=actual,
                             mode="lines", name="Real", line=dict(width=2)))
    fig.add_trace(go.Scatter(x=rec_df["date"], y=rec_df["forecast_central"],
                             mode="lines", name="Pronóstico central", line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=rec_df["date"], y=rec_df["forecast_quantile_95"],
                             mode="lines", name="Cuantil 95", line=dict(dash="dot"),
                             fill="tonexty", fillcolor="rgba(0,100,200,0.1)"))
    fig.update_layout(title="Pronóstico vs Real (periodo de test)",
                      yaxis_title="COP", height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    col_a, col_b = st.columns(2)

    with col_a:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=rec_df["date"], y=idle/1e9, name="Dinero ocioso (B)"))
        fig.add_trace(go.Bar(x=rec_df["date"], y=-shortage/1e9, name="Faltante (B)"))
        fig.update_layout(title="Dinero ocioso y faltante diario",
                          barmode="relative", height=350, yaxis_title="B COP")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        metrics_df = pd.DataFrame({
            "Métrica": ["Dinero ocioso prom.", "Faltante prom.", "Días con faltante",
                        "Nivel de servicio", "Costo total periodo"],
            "Valor": [f"{np.mean(idle)/1e9:.1f}B COP/día",
                      f"{np.mean(shortage)/1e9:.1f}B COP/día",
                      f"{np.mean(shortage > 0)*100:.1f}%",
                      f"{achieved_service:.1f}%",
                      f"{cost_total.sum()/1e6:.1f}M COP"]
        })
        st.table(metrics_df)

# --- Export ---
st.markdown("---")
csv = rec_df.to_csv(index=False)
st.download_button(
    label="📥 Descargar recomendación (CSV)",
    data=csv,
    file_name="recomendacion_liquidez.csv",
    mime="text/csv"
)
