# Valstrat

**Valstrat** é uma engine de simulação estratégica baseada em valuation (DCF) desenvolvida em Python com Flask. O projeto conecta inputs operacionais e quantificação estratégica para gerar projeções financeiras e cenários de valor intrínseco, servindo como ferramenta de estudo para modelagem financeira e análise de negócios.

## Motivação

A premissa central é que estratégia sem números é apenas narrativa, e números sem estratégia são cegos. O **Valstrat** integra essas disciplinas ao exigir que decisões estratégicas (ex: "expansão de mercado") tenham contrapartidas numéricas explícitas nas premissas financeiras, demonstrando o impacto direto na geração de caixa e no valor da empresa.

## Como Funciona

O fluxo de dados segue uma lógica linear:

1.  **Inputs Operacionais**: Entrada de dados históricos e premissas base (Receita, Margens, CAPEX, WACC).
2.  **Ajustes Estratégicos**: Fatores qualitativos (SWOT) são traduzidos em multiplicadores para ajustar as premissas.
3.  **Projeções**: O motor gera o DRE e Fluxo de Caixa Livre (FCF) projetados.
4.  **FCF/DCF**: Cálculo do valor presente dos fluxos e valor terminal (Perpetuidade/Múltiplo).
5.  **Cenários**: Geração automática de cenários (Base, Otimista, Pessimista).
6.  **Insights**: Análise de sensibilidade e impacto das decisões no valuation.

## Estrutura do Projeto

```text
valstrat/
  README.md
  pyproject.toml
  .env.example
  .gitignore
  app.py
  config.py
  engine/
    __init__.py
    model.py
    finance.py
    strategy.py
    scenarios.py
  templates/
    layout.html
    index.html
    results.html
  static/
    css/main.css
    js/main.js
```

## Como Rodar Localmente

1.  **Clone o repositório**:
    ```bash
    git clone https://github.com/seu-usuario/valstrat.git
    cd valstrat
    ```

2.  **Configure o ambiente virtual**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Instale as dependências**:
    ```bash
    # Instalar pacote em modo editável
    pip install -e .
    # (Opcional) Instalar dependências de dev
    pip install -e .[dev]
    ```

4.  **Execute a aplicação**:
    ```bash
    python app.py
    ```
    Acesse no navegador: `http://127.0.0.1:5000`

## Roadmap

1.  Implementar persistência de dados (SQLite) para salvar simulações.
2.  Adicionar exportação de resultados em PDF/Excel.
3.  Criar módulo de Análise de Sensibilidade (Tabela de Dados).
4.  Melhorar a visualização gráfica dos cenários.
5.  Implementar autenticação básica de usuário.

## Disclaimer

**Este software não é uma recomendação de investimento.**

O **Valstrat** é um projeto educacional para simulação de cenários. Os resultados gerados são hipotéticos e dependem inteiramente das premissas inseridas pelo usuário. Não utilize esta ferramenta para tomar decisões financeiras reais. O autor não se responsabiliza por quaisquer perdas ou danos decorrentes do uso deste software.
