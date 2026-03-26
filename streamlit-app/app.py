import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Cafe Origen - Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# DATOS
# ─────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    ventas = pd.read_csv("data/ventas.csv", parse_dates=["fecha"])
    productos = pd.read_csv("data/productos.csv")
    sucursales = pd.read_csv("data/sucursales.csv")

    df = ventas.merge(productos, on="producto_id").merge(sucursales, on="sucursal_id", suffixes=("_prod", "_suc"))
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)
    df["dia_semana"] = df["fecha"].dt.day_name()
    df["hora_dia"] = df["hora"].str[:2].astype(int)
    df["ganancia"] = df["total"] - (df["cantidad"] * df["costo"])
    return df, productos, sucursales

df, productos, sucursales = cargar_datos()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/emoji/96/hot-beverage.png", width=80)
    st.title("Cafe Origen")
    st.caption("Dashboard de Inteligencia de Negocio")
    st.divider()

    # Filtros
    st.subheader("Filtros")

    sucursal_opciones = ["Todas"] + sorted(df["nombre_suc"].unique().tolist())
    sucursal_sel = st.selectbox("Sucursal", sucursal_opciones)

    categoria_opciones = ["Todas"] + sorted(df["categoria"].unique().tolist())
    categoria_sel = st.selectbox("Categoria", categoria_opciones)

    fecha_min = df["fecha"].min().date()
    fecha_max = df["fecha"].max().date()
    rango_fechas = st.date_input(
        "Rango de fechas",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max
    )

    st.divider()
    st.caption("Master Class 2026")
    st.caption("Analisis de Datos con Databricks + IA")

# ─────────────────────────────────────────────
# APLICAR FILTROS
# ─────────────────────────────────────────────
df_filtrado = df.copy()

if sucursal_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["nombre_suc"] == sucursal_sel]

if categoria_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria"] == categoria_sel]

if len(rango_fechas) == 2:
    df_filtrado = df_filtrado[
        (df_filtrado["fecha"].dt.date >= rango_fechas[0]) &
        (df_filtrado["fecha"].dt.date <= rango_fechas[1])
    ]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
# ☕ Cafe Origen — Inteligencia de Negocio
### *"De los datos al grano: decisiones respaldadas por evidencia"*
""")
st.divider()

# ─────────────────────────────────────────────
# KPIs PRINCIPALES
# ─────────────────────────────────────────────
total_ventas = df_filtrado["total"].sum()
num_transacciones = len(df_filtrado)
ticket_promedio = df_filtrado["total"].mean() if num_transacciones > 0 else 0
ganancia_total = df_filtrado["ganancia"].sum()
margen_pct = (ganancia_total / total_ventas * 100) if total_ventas > 0 else 0
dias_operacion = df_filtrado["fecha"].dt.date.nunique()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Ingresos Totales", f"${total_ventas:,.0f}")
col2.metric("Transacciones", f"{num_transacciones:,}")
col3.metric("Ticket Promedio", f"${ticket_promedio:,.0f}")
col4.metric("Ganancia", f"${ganancia_total:,.0f}")
col5.metric("Margen", f"{margen_pct:.1f}%")

st.divider()

# ─────────────────────────────────────────────
# FILA 1: Tendencia + Sucursales
# ─────────────────────────────────────────────
col_izq, col_der = st.columns([3, 2])

with col_izq:
    st.subheader("Tendencia de Ingresos Mensuales")
    df_mes = df_filtrado.groupby("mes").agg(
        ingresos=("total", "sum"),
        transacciones=("total", "count")
    ).reset_index()

    fig_tendencia = px.area(
        df_mes, x="mes", y="ingresos",
        color_discrete_sequence=["#6F4E37"],
        labels={"mes": "Mes", "ingresos": "Ingresos ($)"}
    )
    fig_tendencia.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        height=350
    )
    st.plotly_chart(fig_tendencia, use_container_width=True)

with col_der:
    st.subheader("Ranking de Sucursales")
    df_suc = df_filtrado.groupby("nombre_suc").agg(
        ingresos=("total", "sum"),
        ganancia=("ganancia", "sum")
    ).reset_index().sort_values("ingresos", ascending=True)

    fig_suc = px.bar(
        df_suc, x="ingresos", y="nombre_suc",
        orientation="h",
        color="ingresos",
        color_continuous_scale=["#F5E6D3", "#6F4E37"],
        labels={"nombre_suc": "", "ingresos": "Ingresos ($)"}
    )
    fig_suc.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
        coloraxis_showscale=False,
        height=350
    )
    st.plotly_chart(fig_suc, use_container_width=True)

# ─────────────────────────────────────────────
# FILA 2: Categorias + Metodos de pago
# ─────────────────────────────────────────────
col_izq2, col_der2 = st.columns(2)

with col_izq2:
    st.subheader("Ingresos por Categoria")
    df_cat = df_filtrado.groupby("categoria").agg(
        ingresos=("total", "sum")
    ).reset_index().sort_values("ingresos", ascending=False)

    colores_cat = {
        "bebida_caliente": "#6F4E37",
        "bebida_fria": "#A0785A",
        "panaderia": "#D4A574",
        "comida": "#E8C9A0",
        "otro": "#F5E6D3"
    }
    df_cat["color"] = df_cat["categoria"].map(colores_cat).fillna("#CCC")

    fig_cat = px.pie(
        df_cat, values="ingresos", names="categoria",
        color="categoria",
        color_discrete_map=colores_cat,
        hole=0.4
    )
    fig_cat.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        height=350
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col_der2:
    st.subheader("Metodos de Pago")

    df_pago = df_filtrado.copy()
    df_pago["tipo_pago"] = df_pago["metodo_pago"].map({
        "efectivo": "Efectivo",
        "tarjeta_debito": "Tarjeta Debito",
        "tarjeta_credito": "Tarjeta Credito",
        "nequi": "Nequi",
        "daviplata": "Daviplata"
    })
    df_pago_agg = df_pago.groupby("tipo_pago").agg(
        transacciones=("total", "count"),
        ingresos=("total", "sum")
    ).reset_index().sort_values("transacciones", ascending=False)

    fig_pago = px.bar(
        df_pago_agg, x="tipo_pago", y="transacciones",
        color="tipo_pago",
        color_discrete_sequence=["#6F4E37", "#8B6F47", "#A0785A", "#D4A574", "#F5E6D3"],
        labels={"tipo_pago": "", "transacciones": "Transacciones"}
    )
    fig_pago.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
        height=350
    )
    st.plotly_chart(fig_pago, use_container_width=True)

# ─────────────────────────────────────────────
# FILA 3: Heatmap de actividad
# ─────────────────────────────────────────────
st.subheader("Mapa de Calor: Cuando Vende Mas Cafe Origen?")

dias_orden = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dias_es = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miercoles",
           "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sabado", "Sunday": "Domingo"}

df_heat = df_filtrado.groupby(["dia_semana", "hora_dia"]).size().reset_index(name="ventas")
df_heat["dia_es"] = df_heat["dia_semana"].map(dias_es)
df_heat["dia_orden"] = df_heat["dia_semana"].map({d: i for i, d in enumerate(dias_orden)})

df_pivot = df_heat.pivot_table(index="dia_es", columns="hora_dia", values="ventas", fill_value=0)
# Reordenar dias
orden_es = [dias_es[d] for d in dias_orden if dias_es[d] in df_pivot.index]
df_pivot = df_pivot.reindex(orden_es)

fig_heat = px.imshow(
    df_pivot,
    color_continuous_scale=["#FFF8F0", "#D4A574", "#6F4E37", "#2C1810"],
    labels={"x": "Hora del dia", "y": "Dia", "color": "Ventas"},
    aspect="auto"
)
fig_heat.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=10, b=0),
    height=300
)
st.plotly_chart(fig_heat, use_container_width=True)

# ─────────────────────────────────────────────
# FILA 4: Top productos + Origen del cafe
# ─────────────────────────────────────────────
col_izq3, col_der3 = st.columns([3, 2])

with col_izq3:
    st.subheader("Top 10 Productos Mas Vendidos")
    df_top = df_filtrado.groupby("nombre_prod").agg(
        unidades=("cantidad", "sum"),
        ingresos=("total", "sum"),
        ganancia=("ganancia", "sum")
    ).reset_index().sort_values("unidades", ascending=False).head(10)

    fig_top = px.bar(
        df_top.sort_values("unidades"), x="unidades", y="nombre_prod",
        orientation="h",
        color="ganancia",
        color_continuous_scale=["#F5E6D3", "#6F4E37"],
        labels={"nombre_prod": "", "unidades": "Unidades Vendidas", "ganancia": "Ganancia ($)"}
    )
    fig_top.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_showscale=False,
        height=400
    )
    st.plotly_chart(fig_top, use_container_width=True)

with col_der3:
    st.subheader("Origen del Cafe")
    st.markdown("""
    Cafe Origen trabaja con caficultores de 3 regiones colombianas.
    Cada region aporta un perfil de sabor unico a nuestros productos.
    """)

    df_origen = df_filtrado[df_filtrado["origen_cafe"] != "N/A"]
    if len(df_origen) > 0:
        df_origen_agg = df_origen.groupby("origen_cafe").agg(
            unidades=("cantidad", "sum"),
            ingresos=("total", "sum")
        ).reset_index()

        fig_origen = px.pie(
            df_origen_agg, values="ingresos", names="origen_cafe",
            color_discrete_sequence=["#6F4E37", "#A0785A", "#D4A574"],
            hole=0.5
        )
        fig_origen.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            height=300
        )
        st.plotly_chart(fig_origen, use_container_width=True)

# ─────────────────────────────────────────────
# FILA 5: Recomendaciones de negocio
# ─────────────────────────────────────────────
st.divider()
st.subheader("Recomendaciones para la Gerencia")

# Calcular insights automaticos
mejor_sucursal = df_filtrado.groupby("nombre_suc")["total"].sum().idxmax() if num_transacciones > 0 else "N/A"
mejor_producto = df_filtrado.groupby("nombre_prod")["cantidad"].sum().idxmax() if num_transacciones > 0 else "N/A"
hora_pico = df_filtrado.groupby("hora_dia")["total"].count().idxmax() if num_transacciones > 0 else 0
mejor_margen_prod = df_filtrado.groupby("nombre_prod")["ganancia"].sum().idxmax() if num_transacciones > 0 else "N/A"

# Digital vs efectivo
pago_digital = len(df_filtrado[df_filtrado["metodo_pago"].isin(["nequi", "daviplata"])])
pago_efectivo = len(df_filtrado[df_filtrado["metodo_pago"] == "efectivo"])
digital_supera = pago_digital > pago_efectivo

rec1, rec2, rec3 = st.columns(3)

with rec1:
    st.markdown(f"""
    **Sucursal Estrella**

    *{mejor_sucursal}* lidera en ingresos.
    Replicar su modelo operativo en las demas sucursales.
    """)

with rec2:
    st.markdown(f"""
    **Hora Pico: {hora_pico}:00**

    Concentrar personal y stock en ese horario.
    El producto mas vendido es *{mejor_producto}*.
    """)

with rec3:
    estado_digital = "superan al" if digital_supera else "van creciendo frente al"
    st.markdown(f"""
    **Pagos Digitales**

    Nequi + Daviplata {estado_digital} efectivo.
    Considerar incentivos para pago digital (menor costo operativo).
    """)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align: center; color: #8B6F47; padding: 20px;'>
    <strong>Master Class 2026</strong> | Analisis de Datos con Databricks + IA<br>
    Dashboard generado con Python + Streamlit | Datos analizados en Databricks<br>
    <em>"La IA genera el codigo, tu haces las preguntas correctas"</em>
</div>
""", unsafe_allow_html=True)
