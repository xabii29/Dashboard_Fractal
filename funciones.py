import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from numba import njit
from matplotlib.collections import PolyCollection, LineCollection
import os
import time
import random

carpeta_base = "Fractales_figs"
#################
#### Utilidades #
#################
def guardar(nombre, sub=None):
    carpeta = os.path.join(carpeta_base, sub) if sub else carpeta_base
    os.makedirs(carpeta, exist_ok=True)
    plt.savefig(os.path.join(carpeta, nombre), dpi=600)
    plt.close()

def limpiar_consola(pausa = 0.5):
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(pausa)

def colores(N):
    vals = np.linspace(0,1,N)
    paleta = random.choice(list(plt.colormaps))
    colors = plt.colormaps[paleta]
    colors = colors(vals)
    return colors,paleta

#################
### Cuadrado rotado  ##
#################
@njit
def vertices_recursivo(p1,p2,p3,p4,pasos,c,s,f,vertices, indices):

    if pasos == 0:
        return indices

    vertices[indices[0], 0, 0],vertices[indices[0], 0, 1]  = p1[0],p1[1]
    vertices[indices[0], 1, 0],vertices[indices[0], 1, 1]  = p2[0],p2[1]
    vertices[indices[0], 2, 0],vertices[indices[0], 2, 1]  = p3[0],p3[1]
    vertices[indices[0], 3, 0],vertices[indices[0], 3, 1]  = p4[0],p4[1]

    p1_n = np.array([(p1[0]*c-p1[1]*s)/f , (p1[0]*s+p1[1]*c)/f ])
    p2_n = np.array([(p2[0]*c-p2[1]*s)/f , (p2[0]*s+p2[1]*c)/f ])
    p3_n = np.array([(p3[0]*c-p3[1]*s)/f , (p3[0]*s+p3[1]*c)/f ])
    p4_n = np.array([(p4[0]*c-p4[1]*s)/f , (p4[0]*s+p4[1]*c)/f ])
    
    indices[0] += 1
    
    vertices_recursivo(p1_n,p2_n,p3_n,p4_n,pasos-1,c,s,f,vertices,indices)
    return indices

@njit
def obtener_vertices(pasos,angulo=10):
    vertices = np.zeros((pasos,4,2))
    indices = np.array([0])

    angulo = np.deg2rad(angulo)
    c = np.cos(angulo)
    s = np.sin(angulo)
    f = abs(c) + abs(s)

    p1=np.array([-1.0,-1.0])
    p2=np.array([-1.0,1.0])
    p3=np.array([1.0,1.0])
    p4=np.array([1.0,-1.0])
    vertices_recursivo(p1,p2,p3,p4,pasos,c,s,f,vertices,indices)
    return vertices

def dibuja_cuadrados(pasos):
    fig, ax = plt.subplots(figsize=(6, 6))
        # Fondo blanco inicial con borde negro
    ax.fill_between([-1, 1], -1, 1, color="white", edgecolor="black")
    if pasos > 0:
        # Obtener datos calculados a toda velocidad por Numba
        vertices = obtener_vertices(pasos)
        coleccion = PolyCollection(vertices, facecolors='white', edgecolors='black')
        ax.add_collection(coleccion)
            
        # Configuraciones estéticas de tu código original
        ax.set_aspect('equal')
        fig.suptitle(f"Generaciones: {pasos}", y=0.1, fontsize = 30)
        plt.axis('off')
    
        # Guardar y mostrar
    guardar(f'cuadrado_generaciones_{pasos}.png', "Cuadrados")
    print(f"\nSe generaron las imagenes de Cuadrados para {pasos} generaciones\n\n")
    


#################
# Árbol fractal #
#################
@njit
def mod_rama(x1, y1, angulo=10, alpha=1):
    angulo = np.deg2rad(angulo)
    c = np.cos(angulo)
    s = np.sin(angulo)
    x2 = x1 * c - y1 * s
    y2 = y1 * c + x1 * s
    x2, y2 = x2 * alpha, y2 * alpha
    return x2, y2

@njit
def crear_ramas(p1, p2, pasos, puntos, indices, angulo=10, alpha=1):
    """Crea dos ramas hijas a partir del segmento (x0,y0)→(x1,y1)."""
    if pasos == 0:
        return indices
    
    puntos[indices[0],0] = p1[0]
    puntos[indices[0],1] = p1[1]
    puntos[indices[0],2] = p2[0]
    puntos[indices[0],3] = p2[1]
    
    indices[0] +=1

    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    # Rama izquierda: escalar y rotar +angulo
    x2, y2 = mod_rama(dx, dy, angulo, alpha)
    x2, y2 = x2 + p2[0], y2 + p2[1]
    crear_ramas(p2,np.array([x2,y2]),pasos-1,puntos,indices,angulo, alpha)

    # Rama derecha: escalar y rotar −angulo
    x3, y3 = mod_rama(dx, dy, -angulo, alpha)
    x3, y3 = x3 + p2[0], y3 + p2[1]
    crear_ramas(p2,np.array([x3,y3]),pasos-1,puntos,indices,angulo, alpha)

    return indices

@njit
def vertices_rama(pasos, angulo=10, alpha=1):
    numero_ramas = sum([2**i for i in range(pasos)])
    
    puntos = np.zeros((numero_ramas,4))
    indices = np.array([0])

    p1 = np.array([1.0,0,0])
    p2 = np.array([1.0,1.0])

    crear_ramas(p1, p2, pasos, puntos, indices, angulo, alpha)
    return puntos


def dibuja_arbol(pasos, angulo = 10, alpha = 0.9):
    
    fig,ax = plt.subplots(figsize=(9,6))
    datos_rama = vertices_rama(pasos, angulo, alpha)
    lineas = datos_rama.reshape(-1,2,2)
    l_col = LineCollection(lineas, color ='green', lw = 1)
    ax.add_collection(l_col)
            
        # Configuraciones estéticas de tu código original
    ax.set_aspect('equal')
    ax.autoscale_view()
    fig.suptitle(f"Generaciones: {pasos}", y=0.1, fontsize = 30)
    plt.axis('off')
        
        # Guardar y mostrar
    guardar(f'arbol_generaciones_{pasos}.png', "Arbol")
    print(f"\nSe generaron las imagenes de Arbol para {pasos} generaciones\n\n")

#################
####Sierpinski###
#################

@njit
def calcular_centros_recursivo(x0, x1, y0, y1, pasos, centros, index):
    if pasos == 0:
        return index
    
    L = (x1 - x0) / 3.0
    
    # Guardar las coordenadas del cuadrado central que se va a pintar
    centros[index[0], 0] = x0 + L
    centros[index[0], 1] = x1 - L
    centros[index[0], 2] = y0 + L
    centros[index[0], 3] = y1 - L
    index[0] += 1  # Avanzar el puntero del arreglo
    
    for i in range(3):
        x0c = x0 + i * L
        x1c = x0c + L
        for j in range(3):
            y0c = y0 + j * L
            y1c = y0c + L
            
            # Evitar el centro recursivo
            if not (i == 1 and j == 1):
                calcular_centros_recursivo(x0c, x1c, y0c, y1c, pasos - 1, centros, index)
    return index

@njit
def obtener_todos_los_centros(pasos):
    # La cantidad exacta de cuadrados negros para 'n' pasos sigue la serie geométrica
    total_cuadrados = sum([8**i for i in range(pasos)])
    multiplicador = 3**pasos
    # Matriz para almacenar: [x_min, x_max, y_min, y_max]
    centros = np.zeros((total_cuadrados, 4))
    index = np.array([0]) # Puntero mutable para simular paso por referencia en Numba
    
    calcular_centros_recursivo(0.0, 1.0*multiplicador, 0.0, 1.0*multiplicador, pasos, centros, index)
    return centros


def dibuja_sierpinski(pasos_limite):
    for gen in range(pasos_limite):
        fig, ax = plt.subplots(figsize=(6, 6))
        por = (pasos_limite - gen) /pasos_limite
        # Fondo blanco inicial con borde negro
        ax.fill_between([0, 1], 0, 1, color="white", edgecolor="black")
        
        if gen > 0:
            # Obtener datos calculados a toda velocidad por Numba
            datos_cuadrados = obtener_todos_los_centros(gen)
            
            # Convertir las coordenadas generadas por Numba en vértices de polígonos
            vertices = []
            lines = []
            for k in range(datos_cuadrados.shape[0]):
                xmin, xmax, ymin, ymax = datos_cuadrados[k]
                # Definir las 4 esquinas del cuadrado
                cuadrado = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
                L = xmax - xmin
                l_1= [(xmin,ymax-2*L),(xmin,ymax+L)]
                l_2= [(xmax,ymax-2*L),(xmax,ymax+L)]

                l_3= [(xmax-2*L,ymin),(xmax+L,ymin)]
                l_4= [(xmax-2*L,ymax),(xmax+L,ymax)]
                lines.append(l_1)
                lines.append(l_2)
                lines.append(l_3)
                lines.append(l_4)
                vertices.append(cuadrado)
            
            # Crear la colección y agregarla al eje (un solo llamado de renderizado)
            l_col = LineCollection(lines, color ='black', lw = 1 * por)
            coleccion = PolyCollection(vertices, facecolors='black', edgecolors='black')
            ax.add_collection(l_col)
            ax.add_collection(coleccion)
            
        # Configuraciones estéticas de tu código original
        ax.set_aspect('equal')
        fig.suptitle(f"Generaciones: {gen}", y=0.1, fontsize = 30)
        plt.axis('off')
        
        # Guardar y mostrar
        guardar(f'sierpinski_generaciones_{gen}.png', "Sierpinski")
    print(f"\nSe generaron las imagenes de Sierpinski para {pasos_limite} generaciones\n\n")
