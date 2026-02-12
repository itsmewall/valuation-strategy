from dataclasses import dataclass

@dataclass
class Inputs:
    revenue0: float
    ebit_margin: float
    tax_rate: float
    da_pct: float
    capex_pct: float
    nwc_pct: float
    years: int
    wacc: float
    terminal_g: float
    # Strategy
    moat: int
    competition: int
    supplier_risk: int
    execution: int


@dataclass
class ScenarioResult:
    scenario_name: str
    growth: float
    wacc: float
    pv_fcfs: float
    pv_terminal: float
    enterprise_value: float
    # Series for charts
    revenue_series: list[float]
    fcf_series: list[float]


@dataclass
class Output:
    base: ScenarioResult
    optimistic: ScenarioResult
    pessimistic: ScenarioResult
    terminal_share_base: float
    years_labels: list[int]
    
    # Detailed Analysis
    revenue_final_base: float
    fcf_final_base: float
    fcf_cumulative_base: float
    cagr_base: float
    fcf_margin_final_base: float

    # Sensitivities (Levers)
    delta_margin_plus_2pp: float
    delta_wacc_minus_1pp: float
    delta_growth_plus_1pp: float

    # Qualitative / Insights
    diagnostics: list[dict]
    levers: list[dict]
