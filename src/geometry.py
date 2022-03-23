import pathlib
from typing import Tuple

import numpy as np
from utils.constants import AUTO_CROSS_MIN_SEP, NODES_TOL, X_AXIS, Y_AXIS, ReturnStatus
from utils.custom_errors import AirfoilNotSorted


class Panel:
    def __init__(self):
        self.position = None
        self.x = None
        self.y = None


class Geometry:
    def __init__(self):
        self.n_panels = None
        self.panels = None

    def compute_parameters(self):
        pass


def _ensure_jordan_and_te_le(
    a: Tuple[np.ndarray, Geometry]
) -> Tuple[ReturnStatus, np.ndarray]:
    """ Ensures that the airfoil is defined as a closed line. If the input is the coordinates of the airfoil nodes, it
    checks if the first point is coincident with the last one, otherwise, it adds another node to match this condition.
    If a Geometry object is given, checks if each panel ends at the same coordinate (or closer than a certain tolerance)
    that the next panel starts. It also ensures that there is a node at the leading edge, setting the closest one to
    coordinates (0, 0) if does not exist.

    Args:
        a: airfoil array containing the coordinates of the nodes.

    Returns:
        ok: if True, the given curve was Jordan. Otherwise, the returned array is now Jordan but it was not when passed
            to the function.

    Raises:
        TypeError: When the given array object is neither a Numpy ndarray nor a Geometry instance.
    """
    ok = ReturnStatus(0)

    if isinstance(a, np.ndarray):
        if a[0] != a[-1]:
            a = np.vstack((a, a[0]))
            ReturnStatus = -1
        if [0.0, 0.0] not in a:
            te_closest_idx = np.argmin(a, axis=1)[X_AXIS]
            a[te_closest_idx] = [0.0, 0.0]
            ReturnStatus = 1

    elif isinstance(a, Geometry):
        te_candidates = []
        for panel_idx, panel in enumerate(a.panels):
            if panel.position == a.n_panels:
                if (panel.x - a.panels[0].x) >= NODES_TOL:
                    panel.x = a.panels[0].x
                    ReturnStatus = False
            else:
                if (panel.x - a.panels[panel_idx + 1].x) >= NODES_TOL:
                    panel.x = a.panels[panel_idx + 1].x
                    ReturnStatus = False
                if (panel.y - a.panels[panel_idx + 1].y) >= NODES_TOL:
                    panel.y = a.panels[panel_idx + 1].y
                    ReturnStatus = False
            te_candidates.append(panel.x)
        if 0 not in te_candidates:
            te_closest_idx = np.argmin(te_candidates)
            a[te_closest_idx].x = 0
            a[te_closest_idx].y = 0
            ReturnStatus = False
        if ReturnStatus is False:
            a.compute_parameters()

    else:
        TypeError(
            "The given airfoil must be a ndarray containing the nodes coordinates or already a Geometry object."
            f"It was passed '{type(a)}'"
        )

    return [ReturnStatus, a]


def _ensure_no_autocross(
    a: Tuple[np.ndarray, Geometry]
) -> Tuple[ReturnStatus, np.ndarray]:
    """ Ensures that the airfoil geometry is not crossing itself. It checks if no y coordinate from the lower surface is
    located above the upper surface at the same (or closest) x coordinate.

    Args:
        a: airfoil array containing the coordinates of the nodes.

    Returns:
        ok: if True, the given curve was Jordan. Otherwise, the returned array is now Jordan but it was not when passed
            to the function.

    Raises:
        TypeError: When the given array object is neither a Numpy ndarray nor a Geometry instance.
    """
    ok = ReturnStatus(True)

    if isinstance(a, np.ndarray):
        pass

    elif isinstance(a, Geometry):
        for panel_idx, panel in enumerate(a.panels):
            pass

    else:
        TypeError(
            "The given airfoil must be a ndarray containing the nodes coordinates or already a Geometry object."
            f"It was passed '{type(a)}'"
        )

    return [ok, a]


def _ensure_ordering() -> bool:
    pass


def load_from_file(src: pathlib.Path, has_header: bool = True) -> np.ndarray:
    """ Load the .txt file containing the coordinates x,y of the airfoil nodes. This file must contain each node
    indicating first the x coordinate and then y coordinate with a comma in between. Each node must be placed at a new
    line, and the first line of the document must be the header (no coordinates).

    Coordinates must start from the trailing edge and define the airfoil in clockwise with length normalized along the
    cord (x axis), hence, it must start and end at point (1,0). It also must include the leading edge point at
    coordinates (0, 0). Otherwise, it will be adjusted to match those conditions based on the closest points to them.

    Example with header (without the header, we start directly with x,y coordinates on the first line):
        NACA0012 Airfoil
        1., 0.
        0.99, 0.12
        ...
        0., 0.
        ...
        1., 0.

    Args:
        src: source to the .txt files as its full path or relative path to the script execution location.
        has_header: if True skips the first line of the document. Otherwise, interpret all lines as node coordinates.

    Returns:
        a: loaded airfoil nodes coordinates as Numpy ndarray after applying all requited sanity checks.
    """
    a = np.loadtxt(src, skiprows=1 if has_header else 0)
    ret, a = _ensure_jordan_and_te_le(a=a)
    if not ret:
        print(
            "The loaded airfoil was not Jordan curve or TE condition was not achieved -> Corrected"
        )
    ret, a = _ensure_no_autocross(a=a)
    if not ret:
        print("The loaded airfoil was auto-crossing itself -> Corrected")
    ret, a = _ensure_ordering(a=a)
    assert ret, AirfoilNotSorted(
        "The loaded airfoil was not properly ordered -> Cannot be automatically corrected"
    )
    return a


def create_from_NACA(series: str, n_nodes: int) -> np.ndarray:
    pass


def create_panels_from_nodes() -> np.ndarray:
    pass


def create_panels_from_anchors() -> np.ndarray:
    pass


def resample() -> np.ndarray:
    pass


def rotate_from_cm() -> np.ndarray:
    pass


def save_to_file(dst: pathlib.Path, filanem: str) -> ReturnStatus:
    pass
