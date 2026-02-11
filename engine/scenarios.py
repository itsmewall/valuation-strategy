from .model import ScenarioResult, Inputs, Output
from .strategy import adjust_assumptions
from .finance import project_fcfs, discount, terminal_value

def scenario_multipliers() -> dict[str, tuple[float, float]]:
    """
    Retorna ajustes (delta growth, delta wacc) para cada cenário.
    """
    return {
        "base": (0.0, 0.0),
        "optimistic": (0.02, -0.005),   # +2% growth, -0.5% wacc
        "pessimistic": (-0.02, 0.01),   # -2% growth, +1% wacc
    }

def run_one(inputs: Inputs, name: str, growth: float, wacc: float) -> ScenarioResult:
    # 1. Project cash flows & revenues
    fcfs, revenues = project_fcfs(inputs, growth)  # Modified project_fcfs below to return tuple

    # 2. Discount explicit period
    pv_fcfs = discount(fcfs, wacc)

    # 3. Terminal Value
    # FCF(n+1) approx = FCF(n) * (1 + terminal_g)
    fcf_last = fcfs[-1]
    tv = terminal_value(fcf_last, wacc, inputs.terminal_g)
    
    # discount TV back to present (t=years)
    pv_tv = tv / ((1 + wacc) ** inputs.years)

    ev = pv_fcfs + pv_tv

    return ScenarioResult(
        scenario_name=name,
        growth=growth,
        wacc=wacc,
        pv_fcfs=pv_fcfs,
        pv_terminal=pv_tv,
        enterprise_value=ev,
        revenue_series=revenues,
        fcf_series=fcfs
    )


def run_valuation(inputs: Inputs) -> Output:
    adj = adjust_assumptions(inputs)
    base_growth = adj.growth_base
    base_wacc = max(0.001, inputs.wacc + adj.wacc_adj)

    mult = scenario_multipliers()

    base = run_one(inputs, "Base", base_growth + mult["base"][0], base_wacc + mult["base"][1])
    opt = run_one(
        inputs, "Otimista", base_growth + mult["optimistic"][0], max(0.001, base_wacc + mult["optimistic"][1])
    )
    pes = run_one(
        inputs, "Pessimista", base_growth + mult["pessimistic"][0], max(0.001, base_wacc + mult["pessimistic"][1])
    )

    terminal_share = 0.0
    if base.enterprise_value > 0:
        terminal_share = base.pv_terminal / base.enterprise_value
    
    years_labels = list(range(1, inputs.years + 1))

    return Output(
        base=base, 
        optimistic=opt, 
        pessimistic=pes, 
        terminal_share_base=terminal_share,
        years_labels=years_labels
    )
