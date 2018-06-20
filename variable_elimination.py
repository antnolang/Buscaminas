import itertools

import networkx as nx
import numpy as np
from pgmpy.extern.six.moves import filter, range

from pgmpy.extern.six import string_types
from pgmpy.factors import factor_product
from pgmpy.inference import Inference
from pgmpy.utils import StateNameDecorator

class VariableElimination(Inference):

    @StateNameDecorator(argument='evidence', return_val=None)
    def _variable_elimination(self, variables, operation, evidence=None, elimination_order=None):
        """
        Implementation of a generalized variable elimination.

        Parameters
        ----------
        variables: list, array-like
            variables that are not to be eliminated.
        operation: str ('marginalize' | 'maximize')
            The operation to do for eliminating the variable.
        evidence: dict
            a dict key, value pair as {var: state_of_var_observed}
            None if no evidence
        elimination_order: list, array-like
            list of variables representing the order in which they
            are to be eliminated. If None order is computed automatically.
        """
        if isinstance(variables, string_types):
            raise TypeError("variables must be a list of strings")
        if isinstance(evidence, string_types):
            raise TypeError("evidence must be a list of strings")

        # Dealing with the case when variables is not provided.
        if not variables:
            all_factors = []
            for factor_li in self.factors.values():
                all_factors.extend(factor_li)
            return set(all_factors)

        eliminated_variables = set()
        
        # --MODIFICADO:
        #     Ya que las evidencias son fijas en cada partida,
        #     aplicamos las evidencias de forma permanente en
        #     la red bayesiana, además de aplicarlas sobre la
        #     copia de los factores (working_factors).
        #               
        #     Además inicializamos working_factors solo con
        #     los factores de las variables relevantes:
        #     "Toda variable que no sea antecesor (en la red)
        #     de alguna de las variables de consulta o de
        #     evidencia, es irrelevante para la consulta"
        
        if evidence:
            for evidence_var in evidence:
                for factor in self.factors[evidence_var]:
                    factor_reduced = factor.reduce([(evidence_var, evidence[evidence_var])], inplace=False)
                    for var in factor_reduced.scope():
                        self.factors[var].remove(factor)
                        self.factors[var].append(factor_reduced)
                        
                del self.factors[evidence_var]
                
        # En este problema en concreto:
        #    - Las variables de consulta (que siempre serán variables X)
        #      nunca tendrán padres ==> solo tenemos que calcular los
        #      antecesores de las variables de evidencia.
        #    - Las variables de evidencia son "eliminadas" en el bloque
        #      if-else de arriba ==> dejan de ser variables relevantes
        #    - Las variables X no tienen antecesores, y las variables Y
        #      solo tienen como antecesores sus padres directos
        #      (es decir, no tienen abuelos) ==> no es necesario un
        #      algoritmo recursivo para calcular los antecesores de
        #      las variables de evidencia.
        
        relevant_variables = set(variables)
        for e in evidence.keys():
            parents = self.model.get_parents(e)
            for p in parents:
                relevant_variables.add(p)
                
        working_factors = {node: {factor for factor in self.factors[node] 
                                  if (set(factor.variables).issubset(relevant_variables))}
                           for node in self.factors if node in relevant_variables}
        #
        # --
                
        if not elimination_order:
            # --MODIFICADO: Min-Degree Heuristic. Eliminamos primero
            #     las variables con menos vecinos
            
            ordered_degree = sorted(self.model.degree, key=lambda node: node[1])
            ordered_nodes = [node[0] for node in ordered_degree]
            elimination_order = [var for var in ordered_nodes 
                                 if var not in set(variables).union(set(evidence.keys() if evidence else []))
                                    and var in relevant_variables]
            #
            # --
        elif any(var in elimination_order for var in
                 set(variables).union(set(evidence.keys() if evidence else []))):
            raise ValueError("Elimination order contains variables which are in"
                             " variables or evidence args")
            
        for var in elimination_order:
            # Removing all the factors containing the variables which are
            # eliminated (as all the factors should be considered only once)
            factors = [factor for factor in working_factors[var]
                       if not set(factor.variables).intersection(eliminated_variables)]
            
            phi = factor_product(*factors)
            phi = getattr(phi, operation)([var], inplace=False)
            del working_factors[var]
            for variable in phi.variables:
                working_factors[variable].add(phi)
            eliminated_variables.add(var)

        final_distribution = set()
        for node in working_factors:
            factors = working_factors[node]
            for factor in factors:
                if not set(factor.variables).intersection(eliminated_variables):
                    final_distribution.add(factor)

        query_var_factor = {}
        for query_var in variables:
            phi = factor_product(*final_distribution)
            query_var_factor[query_var] = phi.marginalize(list(set(variables) -
                                                               set([query_var])),
                                                          inplace=False).normalize(inplace=False)
        return query_var_factor


    def query(self, variables, evidence=None, elimination_order=None):
        """
        Parameters
        ----------
        variables: list
            list of variables for which you want to compute the probability
        evidence: dict
            a dict key, value pair as {var: state_of_var_observed}
            None if no evidence
        elimination_order: list
            order of variable eliminations (if nothing is provided) order is
            computed automatically

        Examples
        --------
        >>> from pgmpy.inference import VariableElimination
        >>> from pgmpy.models import BayesianModel
        >>> import numpy as np
        >>> import pandas as pd
        >>> values = pd.DataFrame(np.random.randint(low=0, high=2, size=(1000, 5)),
        ...                       columns=['A', 'B', 'C', 'D', 'E'])
        >>> model = BayesianModel([('A', 'B'), ('C', 'B'), ('C', 'D'), ('B', 'E')])
        >>> model.fit(values)
        >>> inference = VariableElimination(model)
        >>> phi_query = inference.query(['A', 'B'])
        """
        return self._variable_elimination(variables, 'marginalize',
                                          evidence=evidence, elimination_order=elimination_order)


    def max_marginal(self, variables=None, evidence=None, elimination_order=None):
        """
        Computes the max-marginal over the variables given the evidence.

        Parameters
        ----------
        variables: list
            list of variables over which we want to compute the max-marginal.
        evidence: dict
            a dict key, value pair as {var: state_of_var_observed}
            None if no evidence
        elimination_order: list
            order of variable eliminations (if nothing is provided) order is
            computed automatically

        Examples
        --------
        >>> import numpy as np
        >>> import pandas as pd
        >>> from pgmpy.models import BayesianModel
        >>> from pgmpy.inference import VariableElimination
        >>> values = pd.DataFrame(np.random.randint(low=0, high=2, size=(1000, 5)),
        ...                       columns=['A', 'B', 'C', 'D', 'E'])
        >>> model = BayesianModel([('A', 'B'), ('C', 'B'), ('C', 'D'), ('B', 'E')])
        >>> model.fit(values)
        >>> inference = VariableElimination(model)
        >>> phi_query = inference.max_marginal(['A', 'B'])
        """
        if not variables:
            variables = []
        final_distribution = self._variable_elimination(variables, 'maximize',
                                                        evidence=evidence,
                                                        elimination_order=elimination_order)

        # To handle the case when no argument is passed then
        # _variable_elimination returns a dict.
        if isinstance(final_distribution, dict):
            final_distribution = final_distribution.values()
        return np.max(factor_product(*final_distribution).values)

    
    @StateNameDecorator(argument=None, return_val=True)
    def map_query(self, variables=None, evidence=None, elimination_order=None):
        """
        Computes the MAP Query over the variables given the evidence.

        Parameters
        ----------
        variables: list
            list of variables over which we want to compute the max-marginal.
        evidence: dict
            a dict key, value pair as {var: state_of_var_observed}
            None if no evidence
        elimination_order: list
            order of variable eliminations (if nothing is provided) order is
            computed automatically

        Examples
        --------
        >>> from pgmpy.inference import VariableElimination
        >>> from pgmpy.models import BayesianModel
        >>> import numpy as np
        >>> import pandas as pd
        >>> values = pd.DataFrame(np.random.randint(low=0, high=2, size=(1000, 5)),
        ...                       columns=['A', 'B', 'C', 'D', 'E'])
        >>> model = BayesianModel([('A', 'B'), ('C', 'B'), ('C', 'D'), ('B', 'E')])
        >>> model.fit(values)
        >>> inference = VariableElimination(model)
        >>> phi_query = inference.map_query(['A', 'B'])
        """
        elimination_variables = set(self.variables) - set(evidence.keys()) if evidence else set()
        final_distribution = self._variable_elimination(elimination_variables, 'maximize',
                                                        evidence=evidence,
                                                        elimination_order=elimination_order)
        # To handle the case when no argument is passed then
        # _variable_elimination returns a dict.
        if isinstance(final_distribution, dict):
            final_distribution = final_distribution.values()
        distribution = factor_product(*final_distribution)
        argmax = np.argmax(distribution.values)
        assignment = distribution.assignment([argmax])[0]

        map_query_results = {}
        for var_assignment in assignment:
            var, value = var_assignment
            map_query_results[var] = value

        if not variables:
            return map_query_results
        else:
            return_dict = {}
            for var in variables:
                return_dict[var] = map_query_results[var]
            return return_dict

        
    def induced_graph(self, elimination_order):
        """
        Returns the induced graph formed by running Variable Elimination on the network.

        Parameters
        ----------
        elimination_order: list, array like
            List of variables in the order in which they are to be eliminated.

        Examples
        --------
        >>> import numpy as np
        >>> import pandas as pd
        >>> from pgmpy.models import BayesianModel
        >>> from pgmpy.inference import VariableElimination
        >>> values = pd.DataFrame(np.random.randint(low=0, high=2, size=(1000, 5)),
        ...                       columns=['A', 'B', 'C', 'D', 'E'])
        >>> model = BayesianModel([('A', 'B'), ('C', 'B'), ('C', 'D'), ('B', 'E')])
        >>> model.fit(values)
        >>> inference = VariableElimination(model)
        >>> inference.induced_graph(['C', 'D', 'A', 'B', 'E'])
        <networkx.classes.graph.Graph at 0x7f34ac8c5160>
        """
        # If the elimination order does not contain the same variables as the model
        if set(elimination_order) != set(self.variables):
            raise ValueError("Set of variables in elimination order"
                             " different from variables in model")

        eliminated_variables = set()
        working_factors = {node: [factor.scope() for factor in self.factors[node]]
                           for node in self.factors}

        # The set of cliques that should be in the induced graph
        cliques = set()
        for factors in working_factors.values():
            for factor in factors:
                cliques.add(tuple(factor))
        
        # Removing all the factors containing the variables which are
        # eliminated (as all the factors should be considered only once)
        for var in elimination_order:
            factors = [factor for factor in working_factors[var]
                       if not set(factor).intersection(eliminated_variables)]
            phi = set(itertools.chain(*factors)).difference({var})
            cliques.add(tuple(phi))
            del working_factors[var]
            for variable in phi:
                working_factors[variable].append(list(phi))
            eliminated_variables.add(var)

        edges_comb = [itertools.combinations(c, 2)
                      for c in filter(lambda x: len(x) > 1, cliques)]
        return nx.Graph(itertools.chain(*edges_comb))

    
    def induced_width(self, elimination_order):
        """
        Returns the width (integer) of the induced graph formed by running Variable Elimination on the network.
        The width is the defined as the number of nodes in the largest clique in the graph minus 1.

        Parameters
        ----------
        elimination_order: list, array like
            List of variables in the order in which they are to be eliminated.

        Examples
        --------
        >>> import numpy as np
        >>> import pandas as pd
        >>> from pgmpy.models import BayesianModel
        >>> from pgmpy.inference import VariableElimination
        >>> values = pd.DataFrame(np.random.randint(low=0, high=2, size=(1000, 5)),
        ...                       columns=['A', 'B', 'C', 'D', 'E'])
        >>> model = BayesianModel([('A', 'B'), ('C', 'B'), ('C', 'D'), ('B', 'E')])
        >>> model.fit(values)
        >>> inference = VariableElimination(model)
        >>> inference.induced_width(['C', 'D', 'A', 'B', 'E'])
        3
        """
        induced_graph = self.induced_graph(elimination_order)
        return nx.graph_clique_number(induced_graph) - 1