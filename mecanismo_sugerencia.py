
import networkx as nx  # Permite trabajar con grafos
import pgmpy.models as pgmm  # Modelos gráficos de probabilidad
import pgmpy.factors.discrete as pgmf  # Tablas de probabilidades condicionales y
                                       # factores de probabilidad
import pgmpy.inference as pgmi  # Inferencia probabilística exacta

# Para definir la red bayesiana del juego Buscaminas, primero debemos construir el DAG
# Para ello, definimos los vértices y las aristas del grafo.

def generateDAG(n, m):            
    # Añadimos las aristas a la red bayesiana
    # Un vértice del tipo Yij tendrá una arista con otro vértice de la forma Xij si son colidantes
    # Por tanto, vamos a ir recorriendo cada una de las casillas del tablero y creando aristas que una
    # el vértice Y de esa casilla con los vértices X de las casillas colindantes.
    # Los vértices se crean automáticamente.
    DAG = nx.Graph()
    Modelo_Buscaminas = pgmm.BayesianModel()
    for i in range(1,n+1):
        for j in range(1,m+1):
            if i==1:
                if j==1:
                    # Independientemente del tamaño del tablero, el vértice Y11 siempre tiene los mismos vecinos:
                    Modelo_Buscaminas.add_edges_from([('Y11','X21'),
                                          ('Y11','X22'),
                                          ('Y11','X12')])
                    # El vértice Y1,m posee siempre los mismo vecinos: X1,m-1 y X2,m y X2,m-1:
                elif j==m:
                    Modelo_Buscaminas.add_edges_from([('Y1'+str(m),'X1'+str(m-1)),
                                          ('Y1'+str(m),'X2'+str(m)),
                                          ('Y1'+str(m),'X2'+str(m-1))])
                   # En esta rama se añaden las aristas correspondientes a los vértices donde j>1 && j<m:
                else:
                    Modelo_Buscaminas.add_edges_from([('Y1'+str(j),'X'+str(i)+str(j-1)),
                                          ('Y1'+str(j),'X'+str(i)+str(j+1)),
                                          ('Y1'+str(j),'X'+str(i+1)+str(j-1)),
                                          ('Y1'+str(j),'X'+str(i+1)+str(j)),
                                          ('Y1'+str(j),'X'+str(i+1)+str(j+1))])
            elif i==n:
                if j==1:
                    # El vértice Yn,1 posee 3 vecinos que son Xn,2, Xn-1,1 y Xn-1,2:
                    Modelo_Buscaminas.add_edges_from([('Y'+str(n)+str(1),'X'+str(n)+str(2)),
                                          ('Y'+str(n)+str(1),'X'+str(n-1)+str(1)),
                                          ('Y'+str(n)+str(1),'X'+str(n-1)+str(2))])
                   # El vértice Yn,m posee como vecinos los siguientes vértices: Xn,m-1, Xn-1,m y Xn-1,m-1:
                elif j==m:
                    Modelo_Buscaminas.add_edges_from([('Y'+str(n)+str(m),'X'+str(n)+str(m-1)),
                                          ('Y'+str(n)+str(m),'X'+str(n-1)+str(m)),
                                          ('Y'+str(n)+str(m),'X'+str(n-1)+str(m-1))])
                    # Los vecinos de los vértices Yi,j en los que j>1 y j<m son: Xn,j-1, Xn,j+1, Xn-1,j-1, Xn-1,j y Xn-1,j+1:
                else:
                    Modelo_Buscaminas.add_edges_from([('Y'+str(n)+str(j),'X'+str(n)+str(j-1)),
                                          ('Y'+str(n)+str(j),'X'+str(n)+str(j+1)),
                                          ('Y'+str(n)+str(j),'X'+str(n-1)+str(j-1)),
                                          ('Y'+str(n)+str(j),'X'+str(n-1)+str(j)),
                                          ('Y'+str(n)+str(j),'X'+str(n-1)+str(j+1))])
            # En esta rama, añadiremos las aristas de aquellos vértices Yi,j siendo i>1 && i<m. Dentro de esta rama
            # se estudiarán 3 situaciones distintas (3 subramas):
            else:
                # Subrama 1: se añaden las aristas para los vértices Yi,1 y sus correspondientes vecinos
                if j==1:
                    Modelo_Buscaminas.add_edges_from([('Y'+str(i)+str(1),'X'+str(i)+str(2)),
                                          ('Y'+str(i)+str(1),'X'+str(i+1)+str(1)),
                                          ('Y'+str(i)+str(1),'X'+str(i+1)+str(2)),
                                          ('Y'+str(i)+str(1),'X'+str(i-1)+str(1)),
                                          ('Y'+str(i)+str(1),'X'+str(i-1)+str(2))])
                # Subrama 2: se añaden las aristas para los vértices Yi,m y sus correspondientes vecinos
                elif j==m:
                    Modelo_Buscaminas.add_edges_from([('Y'+str(i)+str(m),'X'+str(i)+str(m-1)),
                                          ('Y'+str(i)+str(m),'X'+str(i+1)+str(m)),
                                          ('Y'+str(i)+str(m),'X'+str(i+1)+str(m-1)),
                                          ('Y'+str(i)+str(m),'X'+str(i-1)+str(m)),
                                          ('Y'+str(i)+str(m),'X'+str(i-1)+str(m-1))])
                # Subrama 3: se añaden las aristas para los vértices Yi,j donde 1<j<m y sus correspondientes vecinos
                else:
                    Modelo_Buscaminas.add_edges_from([('Y'+str(i)+str(j),'X'+str(i)+str(j+1)),
                                          ('Y'+str(i)+str(j),'X'+str(i)+str(j-1)),
                                          ('Y'+str(i)+str(j),'X'+str(i+1)+str(j-1)),
                                          ('Y'+str(i)+str(j),'X'+str(i+1)+str(j)),
                                          ('Y'+str(i)+str(j),'X'+str(i+1)+str(j+1)),
                                          ('Y'+str(i)+str(j),'X'+str(i-1)+str(j-1)),
                                          ('Y'+str(i)+str(j),'X'+str(i-1)+str(j)),
                                          ('Y'+str(i)+str(j),'X'+str(i-1)+str(j+1))])
                    
            DAG.add_nodes_from(Modelo_Buscaminas.nodes())
            DAG.add_edges_from(Modelo_Buscaminas.edges())
            
    return DAG

def drawDAG(DAG):
    nx.draw(DAG, with_labels=True, font_weight='bold')
    return True

# Vecinos de la variable Yi,j en el grafo
def neighborsOf(DAG,y):
    neighbors = []
    for node in DAG[y]:
        neighbors.append(node)
    return neighbors

# CPT (Conditional Probability Tables) asociada a las variables de Y
def createCPT(DAG):
    variablesY = []
    CPTs = {}
    for node in DAG.nodes():
        if node[0] == 'Y':
            neighbors = neighborsOf(DAG,node)
            y_CPT = pgmf.TabularCPD(node,len(neighbors)+1,,neighbors,[2 for i in neighbors])