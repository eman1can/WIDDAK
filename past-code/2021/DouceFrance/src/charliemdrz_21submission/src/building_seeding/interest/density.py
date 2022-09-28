import numpy as np

from building_seeding import Districts
from building_seeding.interest import balance
from utils import *


def density(shape, districts, lambdas):
    # type: (tuple, Districts, tuple) -> ndarray
    assert len(shape) == 2 and len(lambdas) == 3
    interest_matrix = np.vectorize(lambda d: balance(d, *lambdas))(districts[:])
    return interest_matrix

