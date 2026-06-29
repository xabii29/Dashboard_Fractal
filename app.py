import streamlit as st
import io
import matplotlib.pyplot as plt
import matplotlib
import funciones as fn  # Aquí importas todo tu trabajo previo
from matplotlib.collections import PolyCollection, LineCollection

try:
    url_profile = st.secrets["linkedin"]
    git_profile = st.secrets["git"]
    url_post = st.secrets["post"]
except Exception:
    url_profile = "https://www.linkedin.com/"
    git_profile = "https://github.com/"
    url_post = "https://www.linkedin.com/"

# 1. Configuración de Matplotlib para entornos web (Evita ventanas flotantes)
matplotlib.use('Agg')

# 2. Configuración de la página web
st.set_page_config(
    page_title="Generador de Fractales",
    page_icon= "🌀",
    layout="centered"
)

# Precompilación rápida al inicio (Evita retrasos en el primer clic de los usuarios)
# Forzamos a Numba a compilar ejecutando una generación baja en segundo plano
_ = fn.obtener_todos_los_centros(1)
_ = fn.obtener_vertices(1, 10)
_ = fn.vertices_rama(1,10,1)

st.sidebar.header("Generador de Fractales")
st.sidebar.header("Configuraciones:")
# Selector del tipo de fractal
tipo_fractal = st.sidebar.selectbox(
    "Selecciona el Fractal:",
    ["Alfombra de Sierpinski", "Árbol Fractal", "Espiral de Cuadrados"]
)

st.sidebar.markdown("---",)

if tipo_fractal == "Alfombra de Sierpinski":
    st.sidebar.subheader("Parámetros de Sierpinski")
    # Ponemos límites prudentes para que la RAM de Streamlit Cloud no sufra (Máx 5 o 6)
    generaciones = st.sidebar.slider("Generaciones:", min_value=1, max_value=5, value=3)
    if st.sidebar.toggle("Colorear: "):
        colorear, paleta = fn.colores(generaciones)
        st.sidebar.write(f"Paleta de colores: {paleta}")
    else:
        colorear = 'Black'
    st.subheader("Alfombra de Sierpinski")
    
    with st.spinner("Tapizando iteraciones..."):
        fig, ax = plt.subplots(figsize=(6, 6))

        mult = 3**(generaciones)
        ax.fill_between([0, 1*mult], 0, 1*mult, color="white", edgecolor="black")
        
        datos = fn.obtener_todos_los_centros(generaciones)
        vertices = [[(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)] for xmin, xmax, ymin, ymax in datos]
        coleccion = PolyCollection(vertices, facecolors=colorear, edgecolors='black')
        ax.add_collection(coleccion)
        
        ax.set_aspect('equal')
        plt.axis('off')

        buf = io.BytesIO()
        fig.savefig(buf,format='png',dpi=300)
        st.pyplot(fig,clear_figure=True,width=True)

elif tipo_fractal == "Árbol Fractal":
    st.sidebar.subheader("Parámetros del Árbol")

    generaciones = st.sidebar.slider("Generaciones:", min_value=1, max_value=20, value=12)
    angulo = st.sidebar.slider("Ángulo de inclinación (°):", min_value=10, max_value=80, value=70, step=5)
    alpha = st.sidebar.slider("Factor de escala:", min_value=0.5, max_value=1.0, value=0.7, step=0.05)

    if st.sidebar.toggle("Colorear: "):
        colorear, paleta = fn.colores(generaciones)
        st.sidebar.write(f"Paleta de colores: {paleta}")
    else:
        colorear = 'Green'
    st.subheader("Árbol Fractal")
    
    with st.spinner("Creando ramas..."):
        fig, ax = plt.subplots(figsize=(9, 6))
    
        datos_rama = fn.vertices_rama(generaciones, angulo, alpha) # Si adaptaste tu función para recibir ángulo/alpha, pásalos aquí
        lineas = datos_rama.reshape(-1,2,2)
        l_col = LineCollection(lineas, color=colorear, lw=1.2)
        ax.add_collection(l_col)
        
        #ax.set_aspect('equal')
        ax.autoscale_view()
        plt.axis('off')

        buf = io.BytesIO()
        fig.savefig(buf,format='png',dpi=300)
        st.pyplot(fig,clear_figure=True,width=True)

elif tipo_fractal == "Espiral de Cuadrados":
    st.sidebar.subheader("Parámetros del Espiral")

    generaciones = st.sidebar.slider("Generaciones (Anidamiento):", min_value=1, max_value=40, value=20)
    angulo_rot = st.sidebar.slider("Ángulo de Rotación Base (°):", min_value=1, max_value=20, value=10)
    sentido = st.sidebar.radio("Sentido de Rotación:",["Izquierda","Derecha"])
    
    if st.sidebar.toggle("Colorear: "):
        colorear, paleta = fn.colores(generaciones)
        st.sidebar.write(f"Paleta de colores: {paleta}")
    else:
        colorear = 'none'
    st.subheader("Espiral de Cuadrados")
    
    with st.spinner("Gira y gira..."):
       
        fig, ax = plt.subplots(figsize=(6, 6))
        angulo_rot = angulo_rot if sentido == "Izquierda" else -angulo_rot
        vertices = fn.obtener_vertices(generaciones, angulo_rot)
        coleccion = PolyCollection(vertices, facecolors=colorear, edgecolors='black')
        ax.add_collection(coleccion)
        
        ax.autoscale_view()
        ax.set_aspect('equal')
        plt.axis('off')
        
        buf = io.BytesIO()
        fig.savefig(buf,format='png',dpi=300)
        st.pyplot(fig,clear_figure=True,width=True)

st.markdown("---")
st.download_button(
    label="Descarga",
    data=buf,
    file_name= tipo_fractal+ ".png",
    mime="image/png",
    width=True
)

st.markdown("---")
st.write("¿Te quedo algo cool? 📸 compartelo en mi post de [LinkedIn]({url_post}).\n")
st.write("O guardalo en tu galeria 👌")

st.write("Mis redes:")
col_lnk, col_git = st.columns(2)

with col_lnk:
    st.html("""
        <a href={url_profile} target="_blank" style="text-decoration: none;">
            <button style="width: 100%; background-color: #0077B5; color: white; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer; font-weight: bold;">
                🔗 LinkedIn
            </button>
        </a>
    """)
with col_git:
    st.html("""
        <a href={git_profile} target="_blank" style="text-decoration: none;">
            <button style="width: 100%; background-color: black; color: white; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer; font-weight: bold;">
                💻 GitHub
            </button>
        </a>
    """)
st.markdown("---")

    

