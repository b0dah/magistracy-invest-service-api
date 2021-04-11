import numpy as np

from utils.math import cal_max, cal_min, get_matrix_currencies_by_days, get_means_profit


def calculate_minimization(analys_time_line, currencies, const):
    profits = get_matrix_currencies_by_days(currencies, analys_time_line)

    means_profit = get_means_profit(profits)

    cov = np.cov(profits)
    parts = np.array([0] * len(currencies))
    print("Matrix cov")
    print(cov)
    general_risk = (cov.dot(parts)).dot(parts.T)
    general_profit = (parts.T).dot(np.array(profits))

    optimize_proportio = cal_min(cov, means_profit, const / 100)

    general_risk = (cov.dot(optimize_proportio)).dot(optimize_proportio.T) ** 0.5
    print(f"General risk: {general_risk}")
    general_profit = (optimize_proportio.T).dot(np.array(means_profit)) * analys_time_line
    print(f"General_profit: {general_profit}")

    result = {
        "general_profit": general_profit * 100,
        "general_risk": general_risk * 100,
        "tools": []
    }

    for i in range(len(currencies)):
        tool = {
            "profit": means_profit[i] * analys_time_line * 100,
            "proportion": optimize_proportio[i] * 100,
            "risk": np.var(profits[i]) * 100,
            "id": currencies[i]
        }
        result["tools"].append(tool)

    print(f"Result: {result}")
    return result, 200


def calculate_maximization(analys_time_line, currencies, const):
    profits = get_matrix_currencies_by_days(currencies, analys_time_line)

    means_profit = get_means_profit(profits)

    cov = np.cov(profits)
    parts = np.array([0] * len(currencies))
    print("Matrix cov")
    print(cov)
    general_risk = (cov.dot(parts)).dot(parts.T)
    general_profit = (parts.T).dot(np.array(profits))

    optimize_proportio = cal_max(cov, means_profit, const)

    general_risk = (cov.dot(optimize_proportio)).dot(optimize_proportio.T) ** 0.5
    print(f"General risk: {general_risk}")
    general_profit = (optimize_proportio.T).dot(np.array(means_profit)) * analys_time_line
    print(f"General_profit: {general_profit}")

    result = {
        "general_profit": general_profit * 100,
        "general_risk": general_risk * 100,
        "tools": []
    }

    for i in range(len(currencies)):
        tool = {
            "profit": means_profit[i] * analys_time_line * 100,
            "proportion": optimize_proportio[i] * 100,
            "risk": np.var(profits[i]) * 100,
            "id": currencies[i]
        }
        result["tools"].append(tool)

    print(f"Result: {result}")
    return result, 200
