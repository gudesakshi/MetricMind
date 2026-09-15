import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from semantic_engine import load_data, kpi, group_metric

def test_profit_definition():
    df = load_data(Path(__file__).resolve().parents[1] / "data" / "sales.csv")
    assert abs(df["Profit"].sum() - (df["Revenue"].sum()-df["Cost"].sum())) < 0.01

def test_revenue_exists():
    df = load_data(Path(__file__).resolve().parents[1] / "data" / "sales.csv")
    assert kpi(df,"revenue") > 0

def test_region_is_approved():
    df = load_data(Path(__file__).resolve().parents[1] / "data" / "sales.csv")
    result = group_metric(df,"Region","revenue")
    assert not result.empty
