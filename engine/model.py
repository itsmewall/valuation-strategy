from dataclasses import dataclass


@dataclass(frozen=True)
class Inputs:
    # Operacional / financeiro
    revenue0: float          # receita atual (ano 0)
    ebit_margin: float       # % (ex: 0.18)
    tax_rate: float          # % (ex: 0.34)
    da_pct: float            # D&A como % da receita
    capex_pct: float         # CAPEX como % da receita
    nwc_pct: float           # variação de NWC como % da receita (simplificado)
    years: int               # horizonte explícito

    # DCF
    wacc: float              # % (ex: 0.12)
    terminal_g: float        # % (ex: 0.03)

    # Estratégico (0-100)
    moat: int
    competition: int
    supplier_risk: int
    execution: int


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    growth: float
    wacc: float
    enterprise_value: float
    pv_fcfs: float
    pv_terminal: float


@dataclass(frozen=True)
class Output:
    base: ScenarioResult
    optimistic: ScenarioResult
    pessimistic: ScenarioResult

    # “insight” rápido
    terminal_share_base: float  # % do EV que vem do terminal (base)
