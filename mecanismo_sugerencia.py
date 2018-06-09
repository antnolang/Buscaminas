
import matplotlib.pyplot as plt
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
    
    Modelo_Buscaminas = pgmm.BayesianModel()
    for i in range(1,n+1):
        for j in range(1,m+1):
            if i==1:
                if j==1:
                    # Independientemente del tamaño del tablero, el vértice Y11 siempre tiene los mismos vecinos:
                    Modelo_Buscaminas.add_edges_from([('X21','Y11'),
                                          ('X22','Y11'),
                                          ('X12','Y11')])
                    # El vértice Y1,m posee siempre los mismo vecinos: X1,m-1 y X2,m y X2,m-1:
                elif j==m:
                    Modelo_Buscaminas.add_edges_from([('X1'+str(m-1),'Y1'+str(m)),
                                          ('X2'+str(m),'Y1'+str(m)),
                                          ('X2'+str(m-1),'Y1'+str(m))])
                   # En esta rama se añaden las aristas correspondientes a los vértices donde j>1 && j<m:
                else:
                    Modelo_Buscaminas.add_edges_from([('X'+str(i)+str(j-1),'Y1'+str(j)),
                                          ('X'+str(i)+str(j+1),'Y1'+str(j)),
                                          ('X'+str(i+1)+str(j-1),'Y1'+str(j)),
                                          ('X'+str(i+1)+str(j),'Y1'+str(j)),
                                          ('X'+str(i+1)+str(j+1),'Y1'+str(j))])
            elif i==n:
                if j==1:
                    # El vértice Yn,1 posee 3 vecinos que son Xn,2, Xn-1,1 y Xn-1,2:
                    Modelo_Buscaminas.add_edges_from([('X'+str(n)+str(2),'Y'+str(n)+str(1)),
                                          ('X'+str(n-1)+str(1),'Y'+str(n)+str(1)),
                                          ('X'+str(n-1)+str(2),'Y'+str(n)+str(1))])
                   # El vértice Yn,m posee como vecinos los siguientes vértices: Xn,m-1, Xn-1,m y Xn-1,m-1:
                elif j==m:
                    Modelo_Buscaminas.add_edges_from([('X'+str(n)+str(m-1),'Y'+str(n)+str(m)),
                                          ('X'+str(n-1)+str(m),'Y'+str(n)+str(m)),
                                          ('X'+str(n-1)+str(m-1),'Y'+str(n)+str(m))])
                    # Los vecinos de los vértices Yi,j en los que j>1 y j<m son: Xn,j-1, Xn,j+1, Xn-1,j-1, Xn-1,j y Xn-1,j+1:
                else:
                    Modelo_Buscaminas.add_edges_from([('X'+str(n)+str(j-1),'Y'+str(n)+str(j)),
                                          ('X'+str(n)+str(j+1),'Y'+str(n)+str(j)),
                                          ('X'+str(n-1)+str(j-1),'Y'+str(n)+str(j)),
                                          ('X'+str(n-1)+str(j),'Y'+str(n)+str(j)),
                                          ('X'+str(n-1)+str(j+1),'Y'+str(n)+str(j))])
            # En esta rama, añadiremos las aristas de aquellos vértices Yi,j siendo i>1 && i<m. Dentro de esta rama
            # se estudiarán 3 situaciones distintas (3 subramas):
            else:
                # Subrama 1: se añaden las aristas para los vértices Yi,1 y sus correspondientes vecinos
                if j==1:
                    Modelo_Buscaminas.add_edges_from([('X'+str(i)+str(2),'Y'+str(i)+str(1)),
                                          ('X'+str(i+1)+str(1),'Y'+str(i)+str(1)),
                                          ('X'+str(i+1)+str(2),'Y'+str(i)+str(1)),
                                          ('X'+str(i-1)+str(1),'Y'+str(i)+str(1)),
                                          ('X'+str(i-1)+str(2),'Y'+str(i)+str(1))])
                # Subrama 2: se añaden las aristas para los vértices Yi,m y sus correspondientes vecinos
                elif j==m:
                    Modelo_Buscaminas.add_edges_from([('X'+str(i)+str(m-1),'Y'+str(i)+str(m)),
                                          ('X'+str(i+1)+str(m),'Y'+str(i)+str(m)),
                                          ('X'+str(i+1)+str(m-1),'Y'+str(i)+str(m)),
                                          ('X'+str(i-1)+str(m),'Y'+str(i)+str(m)),
                                          ('X'+str(i-1)+str(m-1),'Y'+str(i)+str(m))])
                # Subrama 3: se añaden las aristas para los vértices Yi,j donde 1<j<m y sus correspondientes vecinos
                else:
                    Modelo_Buscaminas.add_edges_from([('X'+str(i)+str(j+1),'Y'+str(i)+str(j)),
                                          ('X'+str(i)+str(j-1),'Y'+str(i)+str(j)),
                                          ('X'+str(i+1)+str(j-1),'Y'+str(i)+str(j)),
                                          ('X'+str(i+1)+str(j),'Y'+str(i)+str(j)),
                                          ('X'+str(i+1)+str(j+1),'Y'+str(i)+str(j)),
                                          ('X'+str(i-1)+str(j-1),'Y'+str(i)+str(j)),
                                          ('X'+str(i-1)+str(j),'Y'+str(i)+str(j)),
                                          ('X'+str(i-1)+str(j+1),'Y'+str(i)+str(j))])
            
    return Modelo_Buscaminas

# TODO: Esta funcion, networkx y matplot no-se-que están momentaneamente.
def drawDAG(DAG):
    nxg = nx.Graph()
    nxg.add_nodes_from(DAG.nodes())
    nxg.add_edges_from(DAG.edges())
    nx.draw(nxg, with_labels=True, font_weight='bold')

    #drawDAG(bn)
    #plt.show(bn)
    
def mines_count(j):
    number = format(j, 'b')
    return number.count('1')

# CPD (Conditional Probability Distribution) asociada a las variables de Y
def createCPT(DAG, m, n, num_of_mines):
    for node in DAG.nodes():
        # Cuando hagamos el for también para X, este if sobra.
        if node[0] == 'Y':
            neighbors = list(DAG.get_parents(node))
            num_of_states = len(neighbors)+1
            combinations = 2**len(neighbors)
            y_CPD = pgmf.TabularCPD(node, num_of_states, [[1 if mines_count(j) == i else 0 for j in range(combinations)] for i in range(num_of_states)],neighbors,[2 for n in neighbors])
            DAG.add_cpds(y_CPD)
        elif node[0] == 'X':
            size = m*n
            mine_prob = num_of_mines/size
            no_mine_prob = 1 - mine_prob
            x_CPD = pgmf.TabularCPD(node, 2, [[no_mine_prob, mine_prob]])
            DAG.add_cpds(x_CPD)