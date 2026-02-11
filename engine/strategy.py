from dataclasses import dataclass

from .model import Inputs


@dataclass(frozen=True)
class AdjustedAssumptions:
    growth_base: float
    wacc_adj: float


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def score01(x_0_100: int) -> float:
    return clamp01(x_0_100 / 100.0)


def adjust_assumptions(inputs: Inputs) -> AdjustedAssumptions:
    """
    Tradução simples de “SWOT quantificada” -> premissas.
    MVP: gera um crescimento base e um ajuste no WACC.
    """

    moat = score01(inputs.moat)                 # maior é melhor
    competition = score01(inputs.competition)   # maior é pior
    supplier = score01(inputs.supplier_risk)    # maior é pior
    execution = score01(inputs.execution)       # maior é melhor

    # Crescimento base (regra simples e explicável)
    # Começa em 6% e ajusta por sinais estratégicos
    growth_base = 0.06
    growth_base += 0.06 * (moat - 0.5)
    growth_base += 0.04 * (execution - 0.5)
    growth_base -= 0.05 * (competition - 0.5)
    growth_base -= 0.03 * (supplier - 0.5)

    # Limites razoáveis para MVP
    growth_base = max(-0.05, min(0.30, growth_base))

    # Ajuste de risco no WACC (em pontos percentuais)
    # Moat/execution reduzem, competição/fornecedor aumentam
    wacc_adj = 0.0
    wacc_adj -= 0.02 * (moat - 0.5)
    wacc_adj -= 0.01 * (execution - 0.5)
    wacc_adj += 0.02 * (competition - 0.5)
    wacc_adj += 0.015 * (supplier - 0.5)

    return AdjustedAssumptions(growth_base=growth_base, wacc_adj=wacc_adj)
