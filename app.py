from flask import Flask, render_template, request

from config import Config
from engine.model import Inputs
from engine.scenarios import run_valuation


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/results")
    def results():
        form = request.form

        # MVP: poucos campos, todos numéricos e diretos
        inputs = Inputs(
            revenue0=float(form.get("revenue0", 0) or 0),
            ebit_margin=float(form.get("ebit_margin", 0) or 0),
            tax_rate=float(form.get("tax_rate", 0) or 0),
            da_pct=float(form.get("da_pct", 0) or 0),
            capex_pct=float(form.get("capex_pct", 0) or 0),
            nwc_pct=float(form.get("nwc_pct", 0) or 0),
            years=int(form.get("years", 5) or 5),
            wacc=float(form.get("wacc", 0) or 0),
            terminal_g=float(form.get("terminal_g", 0) or 0),
            # “estratégia” (0 a 100): simples, mas útil para já
            moat=int(form.get("moat", 50) or 50),
            competition=int(form.get("competition", 50) or 50),
            supplier_risk=int(form.get("supplier_risk", 50) or 50),
            execution=int(form.get("execution", 50) or 50),
        )

        out = run_valuation(inputs)
        return render_template("results.html", inputs=inputs, out=out)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config.get("FLASK_DEBUG", True))
