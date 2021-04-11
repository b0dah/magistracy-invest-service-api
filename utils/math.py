from scipy.optimize import minimize
import numpy as np
import ujson


def cal_min(cov, profits, targer):
    def gen_risk(x):
        return (cov.dot(x)).dot(x.T)

    def sum_parts(x):
        return np.sum(x) - 1

    def gen_prof(x):
        print(f"Profit: {(x.T).dot(profits)}")
        return ((x.T).dot(profits)*365) - targer
    

    x0 = np.array([0]*len(cov))
    b = (0.0, 1.0)
    bnds = (b,)*len(cov)
    con1 = {'type': 'eq', 'fun': sum_parts}
    con2 = {'type': 'eq', 'fun': gen_prof}
    cons = [con1, con2]
    sol = minimize(gen_risk, x0, method='SLSQP', bounds=bnds, constraints=cons)
    print(sol)

    return sol.x


def cal_max(cov, profits, const):
    def gen_prof(x):
        return -(x.T).dot(profits)

    def gen_risk(x):
        return (cov.dot(x)).dot(x.T) - const

    def sum_parts(x):
        return np.sum(x) - 1

    x0 = np.array([0]*len(cov))
    b = (0.0, 1.0)
    bnds = (b,)*len(cov)
    con1 = {'type': 'eq', 'fun': sum_parts}
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

    with open('db/charts.json', 'r') as file:
        charts = ujson.loads(file.read())

    mat_profits = np.empty((0, analys_time_line), float)

    for i in range(len(currencies)):
        len_cur = len(charts[currencies[i]]["profits"])
        if len_cur < analys_time_line:
            buf = [0]*(analys_time_line - len_cur)
            mat_profits = np.append(mat_profits, np.array(
                [[*buf, *charts[currencies[i]]["profits"]]]), axis=0)
        else:
            mat_profits = np.append(mat_profits, np.array(
                [charts[currencies[i]]["profits"][len_cur - analys_time_line:]]), axis=0)

    return mat_profits


def get_means_profit(profits):
    means = []
    for i in range(len(profits)):
        means.append(np.mean(list(filter(lambda x: x != 0, profits[i]))))
    return np.array(means)
