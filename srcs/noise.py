from numba import njit
from opensimplex.internals import _noise2, _noise3, _init

from settings import SEED

perm, permGradIndex3D = _init(SEED)

@njit(cache=True)
def noise2(x, y):
    return _noise2(x, y, perm)

@njit(cache=True)
def noise3(x, y, z):
    return _noise3(x, y, z, perm, permGradIndex3D)
