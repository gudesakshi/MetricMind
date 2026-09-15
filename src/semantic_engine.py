"""
MetricMind governed semantic engine.
This local MVP intentionally restricts analysis to approved metrics and dimensions.
"""
import pandas as pd
import numpy as np

APPROVED_METRICS = {
    "revenue": "Revenue",
    "cost": "Cost",
    "profit": "Profit",
    "margin": "Profit_Margin",
    "profit_margin": "Profit_Margin",
    "orders": "Order_ID",
    "quantity": "Quantity",
}

APPROVED_DIMENSIONS = ["Country", "Region", "Product", "Category", "Month"]

def load_data(path="data/sales.csv"):
    df = pd.read_csv(path, parse_dates=["Order_Date"])
    df["Profit"] = df["Revenue"] - df["Cost"]
    df["Profit_Margin"] = np.where(df["Revenue"] != 0, df["Profit"] / df["Revenue"], 0)
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    return df

def kpi(df, metric):
    m = metric.lower()
    if m == "revenue":
        return float(df["Revenue"].sum())
    if m == "cost":
        return float(df["Cost"].sum())
    if m == "profit":
        return float(df["Profit"].sum())
    if m in ("margin", "profit_margin"):
        return float(df["Profit"].sum() / df["Revenue"].sum())
    if m == "orders":
        return int(df["Order_ID"].nunique())
    if m == "quantity":
        return int(df["Quantity"].sum())
    raise ValueError(f"Metric '{metric}' is not approved.")

def group_metric(df, dimension, metric="revenue", top_n=None):
    # Normalize common user terms.
    aliases = {"country":"Country","countries":"Country","region":"Region","product":"Product","category":"Category","month":"Month"}
    dim = aliases.get(dimension.lower(), dimension)
    if dim not in APPROVED_DIMENSIONS:
        raise ValueError(f"Dimension '{dimension}' is not approved.")
    m = metric.lower()
    if m == "revenue":
        s = df.groupby(dim)["Revenue"].sum()
    elif m == "cost":
        s = df.groupby(dim)["Cost"].sum()
    elif m == "profit":
        s = df.groupby(dim)["Profit"].sum()
    elif m in ("margin","profit_margin"):
        s = df.groupby(dim).apply(lambda x: x["Profit"].sum()/x["Revenue"].sum())
    else:
        raise ValueError(f"Metric '{metric}' is not approved.")
    out = s.sort_values(ascending=False).reset_index(name=metric)
    return out.head(top_n) if top_n else out

def monthly_revenue(df):
    out = df.groupby("Month", as_index=False)["Revenue"].sum().sort_values("Month")
    out["MoM_Growth"] = out["Revenue"].pct_change()
    return out

def answer_structured(question, df):
    q = question.lower()
    if "total revenue" in q or ("revenue" in q and "total" in q):
        return {"type":"kpi","metric":"Revenue","value":kpi(df,"revenue"),
                "answer":f"Total revenue is ₹{kpi(df,'revenue'):,.2f}."}
    if "total profit" in q:
        v=kpi(df,"profit")
        return {"type":"kpi","metric":"Profit","value":v,"answer":f"Total profit is ₹{v:,.2f}."}
    if "profit margin" in q and "europe" in q:
        x=df[df["Region"].str.lower()=="europe"]
        v=kpi(x,"margin")
        return {"type":"kpi","metric":"Europe Profit Margin","value":v,
                "answer":f"Europe's profit margin is {v:.2%}."}
    if "highest revenue" in q and "country" in q:
        t=group_metric(df,"Country","revenue",1).iloc[0]
        return {"type":"table","data":group_metric(df,"Country","revenue",5).to_dict("records"),
                "answer":f"{t['Country']} has the highest total revenue at ₹{t['revenue']:,.2f}."}
    if "highest revenue" in q and "product" in q:
        t=group_metric(df,"Product","revenue",1).iloc[0]
        return {"type":"table","data":group_metric(df,"Product","revenue",5).to_dict("records"),
                "answer":f"{t['Product']} has the highest total revenue at ₹{t['revenue']:,.2f}."}
    if "highest revenue" in q and "region" in q:
        t=group_metric(df,"Region","revenue",1).iloc[0]
        return {"type":"table","data":group_metric(df,"Region","revenue",5).to_dict("records"),
                "answer":f"{t['Region']} contributes the most revenue at ₹{t['revenue']:,.2f}."}
    if "month" in q and "revenue" in q:
        t=monthly_revenue(df)
        return {"type":"monthly","data":t.to_dict("records"),
                "answer":"Here is the monthly revenue trend and month-over-month growth."}
    return {"type":"help",
            "answer":"I can answer governed questions about revenue, cost, profit, margin, orders, quantity, countries, regions, products, categories, and monthly trends."}
