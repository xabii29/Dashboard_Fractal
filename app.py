import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
import funciones as fn  # Aquí importas todo tu trabajo previo
from matplotlib.collections import PolyCollection, LineCollection


# 1. Configuración de Matplotlib para entornos web (Evita ventanas flotantes)
matplotlib.use('Agg')

# 2. Configuración de la página web
st.set_page_config(
    page_title="Generador de Fractales",
    layout="centered"
)

# Precompilación rápida al inicio (Evita retrasos en el primer clic de los usuarios)
# Forzamos a Numba a compilar ejecutando una generación baja en segundo plano
_ = fn.obtener_todos_los_centros(1)
_ = fn.obtener_vertices(1, 10)
_ = fn.vertices_rama(1,10,1)

# 3. Encabezado principal
st.title("Generador de Fractales")
st.write("Del lado izquierdo puedes seleccionar el tipo de fractal\n")
st.write("Juega con los colores y los parametros para crear algo lindo :)")

st.markdown("---")

# 4. BARRA LATERAL: Control de Mandos
st.sidebar.header("Configuraciones:")

# Selector del tipo de fractal
tipo_fractal = st.sidebar.selectbox(
    "Selecciona el Fractal:",
    ["Alfombra de Sierpinski", "Árbol Fractal", "Espiral de Cuadrados"]
)

# 5. LÓGICA DINÁMICA POR FRACTAL
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
    
    # Renderizado interactivo
    with st.spinner("Tapizando iteraciones..."):
        # En lugar de guardar en disco, creamos la figura para la web
        fig, ax = plt.subplots(figsize=(6, 6))
        mult = 3**(generaciones)
        ax.fill_between([0, 1*mult], 0, 1*mult, color="white", edgecolor="black")
        
        datos = fn.obtener_todos_los_centros(generaciones)
        
        # Reutilizamos tu misma lógica de dibujo directo al 'ax'
        vertices = [[(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)] for xmin, xmax, ymin, ymax in datos]
        coleccion = PolyCollection(vertices, facecolors=colorear, edgecolors='black')
        ax.add_collection(coleccion)
        
        ax.set_aspect('equal')
        plt.axis('off')
        
        # Le pasamos la figura a Streamlit en lugar de plt.savefig()
        st.pyplot(fig)

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
        
        st.pyplot(fig)

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
        
        st.pyplot(fig)
st.markdown("---")
st.write("¿Te quedo algo cool? 📸 compartelo en mi post de LinkedIn.\n")
st.write("O guardalo en tu galeria 👌")

# 6. SECCIÓN DE CRÉDITOS O CÓDIGO (Ideal para LinkedIn)
st.markdown("---")
with st.expander("❓ FAQ's"):
    st.write("""
    El código de estas funciones esta disponible en mi Github.
    """)