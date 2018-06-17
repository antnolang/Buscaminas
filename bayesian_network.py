import matplotlib.pyplot as plt
import networkx as nx  # Permite trabajar con grafos
import pgmpy.models as pgmm  # Modelos gráficos de probabilidad
import pgmpy.factors.discrete as pgmf  # Tablas de probabilidades condicionales
                                       # y factores de probabilidad
import pgmpy.inference as pgmi  # Inferencia probabilística exacta

# Para definir la red bayesiana del juego Buscaminas, primero debemos construir 
# el DAG
# Para ello, definimos los vértices y las aristas del grafo.

def generateBN(height, width, num_of_mines):
    DAG = generateDAG(height, width)
    createCPDs(DAG, height, width, num_of_mines)
    return DAG

def generateDAG(height, width):            
    # Añadimos las aristas a la red bayesiana
    # Un vértice del tipo Yij tendrá una arista con otro vértice de la forma Xij si son colidantes
    # Por tanto, vamos a ir recorriendo cada una de las casillas del tablero y creando aristas que una
    # el vértice Y de esa casilla con los vértices X de las casillas colindantes.
    # Los vértices se crean automáticamente.
    
    n = height
    m = width
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

# TODO: Esta función y los imports networkx y matplotlib.pyplot están de manera 
#       temporal para poder imprimir el grafo. Eliminar todo esto en la versión final.
def drawDAG(DAG):
    nxg = nx.Graph()
    nxg.add_nodes_from(DAG.nodes())
    nxg.add_edges_from(DAG.edges())
    nx.draw(nxg, with_labels=True, font_weight='bold')
    
    #drawDAG(bn)
    #plt.show(bn)


# Calcula la probabilidad de Y = y dadas las variables X vecinas como evidencia.
#
# + Entradas:
#     - y:    Número entero [0,8]. Estado de la variable Y a la que le queremos 
#             calcular su probabilidad.
#     - comb: Número entero positivo. Si por ejemplo consideramos una variable Y 
#             con 3 vecinos X (x1, x2, x3), tenemos 2^3=8 combinaciones posibles
#             para los estados de estos vecinos X: {000, 001, 010, 011, 100, 101, 
#             110, 111}. El número comb representa cada una de estas 
#             combinaciones (0 = 000, 1 = 001, 2 = 010, 3 = 011, etc.)
#
# + Salida: devuelve la probabilidad calculada. La probabilidad de Y dada las 
#           variables de evidencia X solo puede ser:
#     - 1:   Si el valor de Y es igual que el número de variables X con valor 1
#     - 0:   Si el valor de Y es distinto al número de variables X con valor 1
#
# + Calcular número de variables X con valor 1: Pasamos comb a binario. Ahora 
#   tenemos el estado de todas las variables X vecinas de Y. Contando los 1's 
#   del número binario, obtenemos el número de variables X con valor 1.
def prob_Y(y, comb):
    comb = format(comb, 'b')
    one_count = comb.count('1')
    return float(y == one_count)

def createCPDs(DAG, height, width, num_of_mines):
    for node in DAG.nodes():
        if node[0] == 'Y':
            create_y_CPD(node, DAG)
        elif node[0] == 'X':
            create_x_CPD(node, DAG, height, width, num_of_mines)

def create_y_CPD(node, DAG):
    neighbors = list(DAG.get_parents(node))
    num_of_states = len(neighbors)+1
    combinations = 2**len(neighbors)
    y_CPD = pgmf.TabularCPD(node, num_of_states, 
                            [[prob_Y(ns, comb) for comb in range(combinations)]
                                               for ns in range(num_of_states)
                            ], neighbors, [2 for n in neighbors])
    DAG.add_cpds(y_CPD)
    
def create_x_CPD(node, DAG, height, width, num_of_mines):
    size = width*height
    prob_X = num_of_mines/size
    prob_no_X = 1 - prob_X
    x_CPD = pgmf.TabularCPD(node, 2, [[prob_no_X, prob_X]])
    DAG.add_cpds(x_CPD)
    
def calcule_prob_X(variable_elimination, i, j, evidences):
    var_x = bn_X_name(i,j)
    query = variable_elimination.query([var_x], evidences)
    query_res = query[var_x]
    return query_res.values[0]

def bn_X_name(i, j):
    return 'X' + str(i + 1) + str(j + 1)

def bn_Y_name(i, j):
    return 'Y' + str(i + 1) + str(j + 1)