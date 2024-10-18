# model.py
from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag
import json


def probe_model_5l_profit(data: dict):
    financial_index = latest_financial_index(data)

    result = {
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag(data, financial_index),
            "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag(data, financial_index),
            "ISCR_FLAG": iscr_flag(data, financial_index),
        }
    }
    return result


if __name__ == "__main__":
    with open("data.json", "r") as file:
        data = json.load(file)

    result = probe_model_5l_profit(data["data"])
    print(json.dumps(result, indent=4))
