import numpy as np

def tuple_sub(t1: tuple[float, float], t2: tuple[float, float]):
    """Used for tuple substraction A(a1, a2) - B(b1, b2) = (a1 - b1, a2 - b2)

    Args:
        t1 (tuple[float, float]): minuend tuple
        t2 (tuple[float, float]): subtrahend tuple

    Returns:
        tuple[float, float]: difference
    """
    
    return tuple(map(
        lambda i, j:
            i - j,
        t1,
        t2
    ))
    
def dist_two_points(p1: tuple[float, float], p2: tuple[float, float]):
    """Return the ecludian distance between the two point

    Args:
        p1 (tuple[float, float]): coordinate of one point
        p2 (tuple[float, float]): coordinate of another point

    Returns:
        float: ecludian distance
    """
    
    return np.linalg.norm(tuple_sub(p1, p2))

def dist_line_point(
    line_start: tuple[float, float], 
    line_end: tuple[float, float], 
    point: tuple[float, float]
):
    """get the distance between a line and a point

    Args:
        line_start (tuple[float, float]): coordinate of the start point of the line
        line_end (tuple[float, float]): coordinate of the end point of the line
        point (tuple[float, float]): coordinate of the point

    Returns:
        float: distance between the line and the point
    """
    
    return np.linalg.norm(
        np.cross(
            tuple_sub(
                line_end, 
                line_start
            ), 
            tuple_sub(
                point, 
                line_start
    ))) / np.linalg.norm(
        tuple_sub(
            line_end, 
            line_start
    ))