from .model import Inputs


def project_fcfs(inputs: Inputs, growth: float) -> list[float]:
    """
    FCF simplificado por ano:
    EBIT = Receita * margem
    NOPAT = EBIT * (1 - tax)
    D&A = Receita * da_pct
    CAPEX = Receita * capex_pct
    ΔNWC = Receita * nwc_pct
    FCF = NOPAT + D&A - CAPEX - ΔNWC
    """
    rev = inputs.revenue0
    fcfs: list[float] = []

    for _ in range(inputs.years):
        rev = rev * (1.0 + growth)
        ebit = rev * inputs.ebit_margin
        nopat = ebit * (1.0 - inputs.tax_rate)
        da = rev * inputs.da_pct
        capex = rev * inputs.capex_pct
        dnwc = rev * inputs.nwc_pct
        fcf = nopat + da - capex - dnwc
        fcfs.append(fcf)

    return fcfs


def discount(values: list[float], wacc: float) -> float:
    pv = 0.0
    for t, v in enumerate(values, start=1):
        pv += v / ((1.0 + wacc) ** t)
    return pv


def terminal_value(last_fcf: float, wacc: float, g: float) -> float:
    # Gordon Growth: TV = FCF_{t+1} / (WACC - g)
    fcf_next = last_fcf * (1.0 + g)
    denom = (wacc - g)
    if denom <= 0:
        # Evita explosão; MVP: retorna 0 em caso inválido
        return 0.0
    return fcf_next / denom
