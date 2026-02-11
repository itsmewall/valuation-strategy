from .finance import discount, project_fcfs, terminal_value
from .model import Inputs, Output, ScenarioResult
from .strategy import adjust_assumptions


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
    fcfs = project_fcfs(inputs, growth=growth)
    pv_fcfs = discount(fcfs, wacc=wacc)

    tv = terminal_value(fcfs[-1], wacc=wacc, g=inputs.terminal_g) if fcfs else 0.0
    pv_terminal = tv / ((1.0 + wacc) ** inputs.years)

    ev = pv_fcfs + pv_terminal
    return ScenarioResult(
        name=name,
        growth=growth,
        wacc=wacc,
        enterprise_value=ev,
        pv_fcfs=pv_fcfs,
        pv_terminal=pv_terminal,
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

    return Output(base=base, optimistic=opt, pessimistic=pes, terminal_share_base=terminal_share)
