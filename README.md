# MetricMind — Agentic Semantic BI Engine

## Executive summary
MetricMind is a portfolio MVP for governed conversational business intelligence. A business user asks a natural-language question, the system maps the request to approved business metrics and dimensions, retrieves the corresponding analytical result, and presents a concise business explanation with charts.

## Business problem
Raw Text-to-SQL can produce inconsistent joins, filters, and definitions. For example, two teams can calculate Profit Margin differently. MetricMind centralizes metric definitions in a governed semantic layer.

## Solution
**User → Question/Agent Layer → Semantic Layer → Data → Insight**

Approved metrics:
- Revenue = SUM(revenue)
- Cost = SUM(cost)
- Profit = Revenue − Cost
- Profit Margin = Profit / Revenue
- Orders = distinct order_id
- Quantity = SUM(quantity)

## Dataset
5,000 sales transactions covering multiple countries, regions, products, dates, revenue and cost.

## Portfolio MVP technology
- Python
- Pandas / NumPy
- SQL / PostgreSQL-ready schema
- Governed semantic layer implemented in Python JSON + engine
- Streamlit
- Plotly
- Git/GitHub ready

## How to run
```bash
cd MetricMind_Project
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```

Then open the local Streamlit URL shown in the terminal.

## Example questions
1. What is our total revenue?
2. What is our total profit?
3. Which country has the highest revenue?
4. Which region has the highest revenue?
5. Which product has the highest revenue?
6. How did revenue change month over month?
7. What is Europe's profit margin?
8. Which products have the strongest profit?
9. Compare regions by revenue.
10. Which markets should management investigate?

## Important implementation note
The supplied project document describes enterprise components such as Cube/dbt, Databricks/Snowflake, LangChain/Llama and Next.js. This package implements the **working local MVP first**, because it is easier to run, demonstrate and understand. The semantic layer is real and governed; Cube/dbt, PostgreSQL and an LLM can be swapped in as production upgrades without changing the business metric definitions.

## Project structure
```
MetricMind_Project/
├── data/
│   └── sales.csv
├── excel/
│   └── MetricMind_Excel_Analysis.xlsx
├── sql/
│   ├── 01_schema.sql
│   └── 02_business_questions.sql
├── src/
│   ├── app.py
│   ├── semantic_engine.py
│   ├── semantic_layer.json
│   └── llm_adapter.py
├── tests/
│   └── test_semantic.py
├── docs/
├── requirements.txt
└── README.md
```

## Manager demo flow
1. Open MetricMind.
2. Show KPI cards.
3. Ask: “Which region has the highest revenue?”
4. Ask: “Which product has the highest revenue?”
5. Ask: “How did revenue change month over month?”
6. Explain that the answer is generated from governed metrics, not arbitrary metric definitions.
7. Show the semantic layer file and SQL validation queries.
8. Show the Excel analysis and GitHub repository.

## Limitations of this MVP
- The current question router is intentionally controlled rather than a fully autonomous LLM agent.
- The local app uses the CSV as its data source.
- PostgreSQL schema and SQL are included for the database deployment stage.
- Cube/dbt and production LLM integration are documented as the next enterprise-hardening step.

## Suggested future upgrades
1. PostgreSQL as the runtime database.
2. Cube or dbt Semantic Layer as the external governed metric service.
3. LLM orchestration with strict tool/function calling.
4. Natural-language root-cause analysis.
5. Authentication and row-level security.
6. Deployment to a cloud platform.
