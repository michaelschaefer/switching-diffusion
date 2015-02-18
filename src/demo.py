# -*- coding: utf-8 -*-

import numpy as np

from switchingdiffusion.discretizations import EulerMaruyamaDiscretization
from switchingdiffusion.la import OperatorInterface, VectorSpace
from switchingdiffusion.problem import ProblemDescription
from switchingdiffusion.stochasticprocesses import DiscreteTimeMarkovChain
from switchingdiffusion.visualization import visualize_trajectory_1d


class DiffusionOperator(OperatorInterface):

    def __init__(self, dim):
        super(DiffusionOperator, self).__init__()
        self._dim = dim
        self._source = VectorSpace((dim,))
        self._range = VectorSpace((dim,))

    def apply(self, u, r=None):
        assert r is None or isinstance(r, (float, int))
        if r is None:
            return self._range.ones()
        else:
            return self._range.ones() * r


class DriftOperator(OperatorInterface):

    def __init__(self, dim):
        super(DriftOperator, self).__init__()
        self._dim = dim
        self._source = VectorSpace((dim,))
        self._range = VectorSpace((dim,))

    def apply(self, u, r=None):
        return self._range.ones()


class MarkovChainGenerator(OperatorInterface):

    def __init__(self):
        super(MarkovChainGenerator, self).__init__()
        self._dim = 2
        self._source = VectorSpace((self._dim,))
        self._range = VectorSpace((self._dim,)*2)

    def apply(self, u, r=None):
        return np.array([[-10, 10], [10, -10]])


spacial_dimension = 1

markov_generator = MarkovChainGenerator()
markov_chain = DiscreteTimeMarkovChain(2, 0, markov_generator)

diffusion = DiffusionOperator(spacial_dimension)
drift = DriftOperator(spacial_dimension)
initial_condition = np.zeros((spacial_dimension,))
problem = ProblemDescription(drift, diffusion, markov_chain, initial_condition)

discretization = EulerMaruyamaDiscretization(problem, time_range=(0, 1), time_intervals=1000)
trajectory, states = discretization.solve(return_states=True)
visualize_trajectory_1d(trajectory, states=states, discretization=discretization)