# rules.py
import datetime


class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # diplay purpose only
    WHITE = 4  # data is missing for this field


def latest_financial_index(data: dict):
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0


def total_revenue(data: dict, financial_index):
    return data["financials"][financial_index]["pnl"]["lineItems"].get("net_revenue", 0)


def total_borrowing(data: dict, financial_index):
    total_borrowings = data["financials"][financial_index]["bs"]["liabilities"].get("short_term_borrowings", 0)
    total_borrowings += data["financials"][financial_index]["bs"]["liabilities"].get("long_term_borrowings", 0)
    total_revenue_value = total_revenue(data, financial_index)
    return total_borrowings / total_revenue_value if total_revenue_value else 0


def iscr_flag(data: dict, financial_index):
    isr = iscr(data, financial_index)
    return FLAGS.GREEN if isr >= 2 else FLAGS.RED


def total_revenue_5cr_flag(data: dict, financial_index):
    return FLAGS.GREEN if total_revenue(data, financial_index) >= 5000000 else FLAGS.RED


def iscr(data: dict, financial_index):
    pnl = data["financials"][financial_index]["pnl"]["lineItems"]
    profit_before_interest_and_tax = pnl.get("profit_before_interest_and_tax", 0)
    depreciation = pnl.get("depreciation", 0)
    interest = pnl.get("interest", 0)
    return (profit_before_interest_and_tax + depreciation + 1) / (interest + 1)


def borrowing_to_revenue_flag(data: dict, financial_index):
    ratio = total_borrowing(data, financial_index)
    return FLAGS.GREEN if ratio <= 0.25 else FLAGS.AMBER
