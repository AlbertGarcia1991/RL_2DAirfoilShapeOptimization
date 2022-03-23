from enum import Enum

NODES_TOL = 1e-8
AUTO_CROSS_MIN_SEP = 1e-3

X_AXIS = 0
Y_AXIS = 1


class ReturnStatus(Enum):
    _OK = 0
    _ERROR_FIXED = -1
