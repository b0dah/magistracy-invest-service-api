import numpy as np
import ujson
from scipy.optimize import minimize


def cal_min_risk(cov_matrix, mean_profit, target_profit):
    num_assets = len(mean_profit)

    def gen_risk(x):
        risk = np.sqrt((cov_matrix.dot(x)).dot(x.T))
        print(f"Risk: {risk}")
        print("Check the functionality")
        return risk

    x0 = num_assets * [1. / num_assets, ]
    bnds = tuple((0, 1) for asset in range(num_assets))
    con1 = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    con2 = {'type': 'eq', 'fun': lambda x: np.sum(mean_profit * x) * 365 - target_profit}
    cons = [con1, con2]
    if target_profit == 0.0:
        cons = [con1]

    sol = minimize(gen_risk, x0, method='SLSQP', bounds=bnds, constraints=cons)
    print(sol)

    return sol.x


def cal_max_prof(cov_matrix, mean_profit, target_risk):
    num_assets = len(mean_profit)

    def gen_prof(x):
        return -np.sum(mean_profit * x) * 365

    x0 = num_assets * [1. / num_assets, ]
    bnds = tuple((0, 1) for asset in range(num_assets))
    con1 = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    con2 = {'type': 'eq', 'fun': lambda x: np.sqrt((cov_matrix.dot(x)).dot(x.T))- target_risk}

    cons = [con1, con2]
    if target_risk == 0.0:
        cons = [con1]

    sol = minimize(gen_prof, x0, method='SLSQP', bounds=bnds, constraints=cons)
    print(sol)

    return sol.x


def get_matrix_currencies_by_days(currencies, analys_time_line):
    """ 
    Read quotes from the file.
    Create an array by analysis timeline and extract necessities data in a new array.
    Return matrix profits
    """

    with open('data/db/charts.json', 'r') as file:
        charts = ujson.loads(file.read())

    mat_profits = np.empty((0, analys_time_line), float)

    for i in range(len(currencies)):
        len_cur = len(charts[currencies[i]]["profits"])
        if len_cur < analys_time_line:
            raise ValueError(f"Currency {charts[currencies[i]]} don't have enough days to analyse")
        else:
            mat_profits = np.append(mat_profits, np.array(
                [charts[currencies[i]]["profits"][len_cur - analys_time_line:]]), axis=0)

    return mat_profits


def get_means_profit(profits):
    means = []
    for i in range(len(profits)):
        means.append(np.mean(profits[i]))
    return np.array(means)
