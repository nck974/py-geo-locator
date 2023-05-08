
import math


def dd_to_dms(degrees) -> tuple[bool, tuple[float, float, float]]:
    """
    Convert decimal degrees to (deg, min, sec)
    """
    neg = degrees < 0
    degrees = (-1) ** neg * degrees
    degrees, d_int = math.modf(degrees)
    mins, m_int = math.modf(60 * degrees)
    secs        =           round(60 * mins, 2)
    return neg, (d_int, m_int, secs)
