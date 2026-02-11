from .model import Inputs

def project_fcfs(inputs: Inputs, growth: float) -> tuple[list[float], list[float]]:
    """
    Returns (fcfs_list, revenue_list)
    """
    rev = inputs.revenue0
    fcfs: list[float] = []
    revenues: list[float] = []

    for _ in range(inputs.years):
        rev = rev * (1.0 + growth)
        ebit = rev * inputs.ebit_margin
        nopat = ebit * (1.0 - inputs.tax_rate)
        da = rev * inputs.da_pct
        capex = rev * inputs.capex_pct
        dnwc = rev * inputs.nwc_pct
        fcf = nopat + da - capex - dnwc
        
        fcfs.append(fcf)
        revenues.append(rev)

    return fcfs, revenues


def discount(flows: list[float], r: float) -> float:
    pv = 0.0
    for i, flow in enumerate(flows):
        t = i + 1
        pv += flow / ((1 + r) ** t)
    return pv


def terminal_value(fcf_n: float, wacc: float, g: float) -> float:
    # Gordon Growth Model: TV = FCF(n+1) / (WACC - g)
    # Ensure WACC > g for sanity (or clamp denom)
    denom = max(0.001, wacc - g)
    fcf_next = fcf_n * (1 + g)
    return fcf_next / denom
