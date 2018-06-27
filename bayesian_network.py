import pgmpy.models as pgmm
import pgmpy.factors.discrete as pgmf


def generate_BN(height, width, num_of_mines):
    DAG = generate_DAG(height, width)
    
    createCPDs(DAG, height, width, num_of_mines)
    
    return DAG


def generate_DAG(height, width):            
    n = height
    m = width
    modelo_buscaminas = pgmm.BayesianModel()
    
    for i in range(1,n+1):
        for j in range(1,m+1):
            if i==1:
                if j==1:
                    # El vértice Y11 siempre tiene los mismos
                    # vecinos: X21, X22 y X12
                    modelo_buscaminas.add_edges_from([('X21', 'Y11'),
                                                      ('X22', 'Y11'),
                                                      ('X12', 'Y11')])
                elif j==m:
                    # El vértice Y1,m posee siempre los mismos
                    # vecinos: X1,m-1 y X2,m y X2,m-1:
                    modelo_buscaminas.add_edges_from([('X1'+str(m-1), 'Y1'+str(m)),
                                                      ('X2'+str(m), 'Y1'+str(m)),
                                                      ('X2'+str(m-1), 'Y1'+str(m))])
                else:
                    # Se añaden las aristas correspondientes a
                    # los vértices Y1,j donde se cumple que 1<j<m
                    modelo_buscaminas.add_edges_from([('X'+str(i)+str(j-1), 'Y1'+str(j)),
                                                      ('X'+str(i)+str(j+1), 'Y1'+str(j)),
                                                      ('X'+str(i+1)+str(j-1), 'Y1'+str(j)),
                                                      ('X'+str(i+1)+str(j), 'Y1'+str(j)),
                                                      ('X'+str(i+1)+str(j+1), 'Y1'+str(j))])
            elif i==n:
                if j==1:
                    # El vértice Yn,1 posee 3 vecinos que son:
                    # Xn,2, Xn-1,1 y Xn-1,2:
                    modelo_buscaminas.add_edges_from([('X'+str(n)+str(2), 'Y'+str(n)+str(1)),
                                                      ('X'+str(n-1)+str(1), 'Y'+str(n)+str(1)),
                                                      ('X'+str(n-1)+str(2), 'Y'+str(n)+str(1))])
                elif j==m:
                    # El vértice Yn,m posee como vecinos los
                    # siguientes vértices: Xn,m-1, Xn-1,m y Xn-1,m-1
                    modelo_buscaminas.add_edges_from([('X'+str(n)+str(m-1), 'Y'+str(n)+str(m)),
                                                      ('X'+str(n-1)+str(m), 'Y'+str(n)+str(m)),
                                                      ('X'+str(n-1)+str(m-1), 'Y'+str(n)+str(m))])
                else:
                    # Los vecinos de los vértices Yn,j en los que
                    # 1<j<m son: Xn,j-1, Xn,j+1, Xn-1,j-1, Xn-1,j y Xn-1,j+1
                    modelo_buscaminas.add_edges_from([('X'+str(n)+str(j-1), 'Y'+str(n)+str(j)),
                                                      ('X'+str(n)+str(j+1), 'Y'+str(n)+str(j)),
                                                      ('X'+str(n-1)+str(j-1), 'Y'+str(n)+str(j)),
                                                      ('X'+str(n-1)+str(j), 'Y'+str(n)+str(j)),
                                                      ('X'+str(n-1)+str(j+1), 'Y'+str(n)+str(j))])  
            else:
                # En esta rama, añadiremos las aristas de
                # aquellos vértices Yi,j siendo 1<i<m. 
                if j==1:
                    # Subrama 1: se añaden las aristas para los
                    # vértices Yi,1 y sus correspondientes vecinos
                    modelo_buscaminas.add_edges_from([('X'+str(i)+str(2), 'Y'+str(i)+str(1)),
                                                      ('X'+str(i+1)+str(1), 'Y'+str(i)+str(1)),
                                                      ('X'+str(i+1)+str(2), 'Y'+str(i)+str(1)),
                                                      ('X'+str(i-1)+str(1), 'Y'+str(i)+str(1)),
                                                      ('X'+str(i-1)+str(2), 'Y'+str(i)+str(1))])
                elif j==m:
                    # Subrama 2: se añaden las aristas para los
                    # vértices Yi,m y sus correspondientes vecinos
                    modelo_buscaminas.add_edges_from([('X'+str(i)+str(m-1), 'Y'+str(i)+str(m)),
                                                      ('X'+str(i+1)+str(m), 'Y'+str(i)+str(m)),
                                                      ('X'+str(i+1)+str(m-1), 'Y'+str(i)+str(m)),
                                                      ('X'+str(i-1)+str(m), 'Y'+str(i)+str(m)),
                                                      ('X'+str(i-1)+str(m-1), 'Y'+str(i)+str(m))])
                else:
                    # Subrama 3: se añaden las aristas para los
                    # vértices Yi,j donde 1<j<m y sus correspondientes vecinos
                    modelo_buscaminas.add_edges_from([('X'+str(i)+str(j+1), 'Y'+str(i)+str(j)),
                                                      ('X'+str(i)+str(j-1), 'Y'+str(i)+str(j)),
                                                      ('X'+str(i+1)+str(j-1), 'Y'+str(i)+str(j)),
                                                      ('X'+str(i+1)+str(j), 'Y'+str(i)+str(j)),
                                                      ('X'+str(i+1)+str(j+1), 'Y'+str(i)+str(j)),
                                                      ('X'+str(i-1)+str(j-1), 'Y'+str(i)+str(j)),
                                                      ('X'+str(i-1)+str(j), 'Y'+str(i)+str(j)),
                                                      ('X'+str(i-1)+str(j+1), 'Y'+str(i)+str(j))])         
    
    return modelo_buscaminas
    

# Calcula la probabilidad de Y = y dados los valores de las
# variables X vecinas (codificadas en "comb") como evidencia:
#     - 1.0: Si y == número de variables X con valor 1
#     - 0.0: Si y != número de variables X con valor 1
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
                            ],
                            neighbors,
                            [2 for n in neighbors])
    
    DAG.add_cpds(y_CPD)
    
    
def create_x_CPD(node, DAG, height, width, num_of_mines):
    size = width*height
    prob_X = num_of_mines/size
    prob_no_X = 1 - prob_X
    
    x_CPD = pgmf.TabularCPD(node, 2, [[prob_no_X, prob_X]])
    
    print(x_CPD)
    DAG.add_cpds(x_CPD)

    
def calcule_prob_X(variable_elimination, i, j, evidences):
    var_x = bn_X_name(i,j)
    
    query = variable_elimination.query([var_x], evidences)
    query_res = query[var_x]
    
    return query_res.values[0]


def bn_X_name(i, j):
    return 'X' + str(i+1) + str(j+1)


def bn_Y_name(i, j):
    return 'Y' + str(i+1) + str(j+1)