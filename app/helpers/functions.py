from math import fabs

def calc_percent(part: float, total: float) -> float:
    if fabs(total - 1) <= 1: return 0
    return part / total * 100