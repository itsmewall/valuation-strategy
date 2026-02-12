from .model import ScenarioResult, Inputs, Output
from .strategy import adjust_assumptions
from .finance import project_fcfs, discount, terminal_value
import dataclasses

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

    # --- EXTENDED ANALYSIS ---
    
    # A) Base Metrics
    revenue_final = base.revenue_series[-1]
    fcf_final = base.fcf_series[-1]
    fcf_cumulative = sum(base.fcf_series)
    # Avoid div by zero if years=0
    if inputs.years > 0:
        cagr = (revenue_final / max(1.0, inputs.revenue0)) ** (1.0 / inputs.years) - 1.0
    else:
        cagr = 0.0
    
    fcf_margin_final = 0.0
    if revenue_final > 0:
        fcf_margin_final = fcf_final / revenue_final

    # B) Mini Sensitivities (Levers)
    # 1. Margin +2pp
    inputs_margin_up = dataclasses.replace(inputs, ebit_margin=min(0.90, inputs.ebit_margin + 0.02))
    scen_margin_up = run_one(inputs_margin_up, "Margin+", base_growth, base_wacc)
    delta_margin = scen_margin_up.enterprise_value - base.enterprise_value

    # 2. WACC -1pp
    wacc_down_final = max(0.001, base_wacc - 0.01)
    scen_wacc_down = run_one(inputs, "WACC-", base_growth, wacc_down_final)
    delta_wacc = scen_wacc_down.enterprise_value - base.enterprise_value

    # 3. Growth +1pp
    growth_up = min(0.30, base_growth + 0.01)
    scen_growth_up = run_one(inputs, "Growth+", growth_up, base_wacc)
    delta_growth = scen_growth_up.enterprise_value - base.enterprise_value

    # C) Diagnostics
    diagnostics = []

    # Rule 1: High Terminal Value dependency
    if terminal_share > 0.60:
        diagnostics.append({
            "title": "Dependência do longo prazo",
            "explanation": f"{terminal_share:.1%} do valor vem da perpetuidade."
        })
    
    # Rule 2: High WACC
    if base_wacc > 0.15:
        diagnostics.append({
            "title": "Risco caro",
            "explanation": f"WACC de {base_wacc:.1%} comprime o valuation."
        })

    # Rule 3: Heavy Reinvestment
    reinvestment_rate = inputs.capex_pct + inputs.nwc_pct
    if reinvestment_rate > 0.15:
        diagnostics.append({
            "title": "Crescimento consome caixa",
            "explanation": f"Reinvestimento de {reinvestment_rate:.1%} limita fluxo livre."
        })

    # Rule 4: Low Margins
    if inputs.ebit_margin < 0.10:
        diagnostics.append({
            "title": "Margem fraca",
            "explanation": f"Margem de {inputs.ebit_margin:.1%} é baixa."
        })
    
    # Limit to 3
    diagnostics = diagnostics[:3]

    # D) Levers
    levers = [
        {
            "title": "Margem +2pp",
            "impact": delta_margin,
            "pct": (delta_margin / base.enterprise_value) if base.enterprise_value else 0.0,
            "description": "Melhora operacional direta."
        },
        {
            "title": "Risco -1pp",
            "impact": delta_wacc,
            "pct": (delta_wacc / base.enterprise_value) if base.enterprise_value else 0.0,
            "description": "Menor custo de capital."
        },
        {
            "title": "Crescimento +1pp",
            "impact": delta_growth,
            "pct": (delta_growth / base.enterprise_value) if base.enterprise_value else 0.0,
            "description": "Expansão de vendas."
        }
    ]
    # Sort levers by impact desc
    levers.sort(key=lambda x: x["impact"], reverse=True)


    return Output(
        base=base, 
        optimistic=opt, 
        pessimistic=pes, 
        terminal_share_base=terminal_share,
        years_labels=years_labels,
        
        # New Fields
        revenue_final_base=revenue_final,
        fcf_final_base=fcf_final,
        fcf_cumulative_base=fcf_cumulative,
        cagr_base=cagr,
        fcf_margin_final_base=fcf_margin_final,

        delta_margin_plus_2pp=delta_margin,
        delta_wacc_minus_1pp=delta_wacc,
        delta_growth_plus_1pp=delta_growth,

        diagnostics=diagnostics,
        levers=levers
    )
