# Valuation Strategy

**Valuation Strategy** é uma engine de simulação estratégica baseada em valuation (DCF) integrada a uma interface web simples. O projeto conecta inputs operacionais e fatores estratégicos quantificados (estilo SWOT) para ajustar premissas financeiras, gerando projeções de fluxo de caixa e múltiplos cenários de valor intrínseco.

## Motivação

Estratégia sem números é apenas narrativa; números sem estratégia são cegos. 
Muitos modelos de valuation falham ao tratar a estratégia como um "anexo qualitativo". O **Valuation Strategy** torna a estratégia parte integrante do modelo matemático: cada decisão estratégica (ex: "Expansão agressiva") deve ter uma contrapartida numérica explícita (ex: "+X% receita, -Y% margem"), forçando a consistência entre a visão de negócio e a realidade financeira.

## Como Funciona

O fluxo de dados segue uma lógica linear e causal:

1.  **Inputs Base**: O usuário insere dados históricos e premissas operacionais iniciais (Receita, Margens, CAPEX, WACC).
2.  **Ajustes Estratégicos**: Fatores qualitativos (Forças, Fraquezas, Oportunidades, Ameaças) são traduzidos em multiplicadores numéricos.
3.  **Projeções**: O sistema aplica os ajustes às premissas base para projetar o DRE e Fluxo de Caixa Livre (FCF) para os próximos anos.
4.  **Valuation (DCF)**:
    *   Cálculo do valor presente dos fluxos explícitos.
    *   Cálculo do valor terminal (Perpetuidade).
    *   Desconto pelo WACC ajustado ao risco da estratégia.
5.  **Cenários e Insights**: Geração automática de cenários (Base, Otimista, Pessimista) para análise de sensibilidade e tomada de decisão.

## Estrutura do Projeto

A organização é flat e modular para manter a simplicidade:

```text
valuation-strategy/
├── engine/          # Núcleo da lógica de negócio
│   ├── model.py     # Classes de projeção e valuation
│   ├── finance.py   # Funções utilitárias financeiras
│   ├── strategy.py  # Lógica de quantificação estratégica
│   └── scenarios.py # Gerador de cenários
├── static/          # Assets (CSS, JS)
├── templates/       # Arquivos HTML (Jinja2)
├── config.py        # Configurações da aplicação Flask
├── run.py           # Ponto de entrada (Entrypoint)
└── pyproject.toml   # Gerenciamento de dependências
```

## Como Rodar Localmente

Pré-requisitos: Python 3.11+.

1.  **Clone o repositório e entre na pasta**:
    ```bash
    git clone https://github.com/itsmewall/valuation-strategy.git
    cd valuation-strategy
    ```

2.  **Crie e ative o ambiente virtual**:
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências**:
    ```bash
    pip install .
    # Ou para desenvolvimento (com pytest/ruff):
    pip install .[dev]
    ```

4.  **Configure as variáveis de ambiente (opcional)**:
    Copie o arquivo de exemplo:
    ```bash
    cp .env.example .env
    ```

5.  **Execute a aplicação**:
    ```bash
    python run.py
    ```
    Acesse em: `http://127.0.0.1:5000`

## Roadmap

*   Implementar testes unitários para o módulo `engine`.
*   Adicionar persistência leve (SQLite) para salvar simulações.
*   Criar funcionalidade de exportação de relatórios (PDF/Excel).
*   Melhorar a visualização de sensibilidade (Tabela de Dados).

## Disclaimer

**Este projeto tem fins estritamente educacionais e de portfólio.**

O **Valuation Strategy** é uma ferramenta de simulação e não deve ser utilizado como base única para decisões reais de investimento, fusão ou aquisição. O autor não se responsabiliza por perdas financeiras decorrentes do uso deste software.
