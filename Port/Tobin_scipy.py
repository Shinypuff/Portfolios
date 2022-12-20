from scipy.optimize import minimize
import numpy as np

class TobinPortfolio:
    def __init__(self, returns, cov_mat, risk_det=None, args=None):
        self.returns = returns
        self.cov_mat = cov_mat
        if risk_det is not None:
            self.risk_det = risk_det
        elif args is not None and 'risk_det' in args.keys():
            self.risk_det = args['risk_det']
        else:
            raise ValueError('risk_det or args must be set')

    def fit(self):

        def objective(x):  # функция доходности
            return - self.returns.T @ np.array(x)

        def constraint1(x):  # условие для суммы долей -1
            return 1.0 - np.sum(np.array(x))

        def constraint2(x):  # задание риска
            return self.risk_det - np.array(x).T @ self.cov_mat @ np.array(x)

        n = len(self.returns)
        x0 = [1/n]*n  # начальное значение переменных для поиска минимума функции риска
        b = (0.0, 0.1)  # условие для  x от нуля до единицы включая пределы
        bnds = [b] * n  # передача условий в функцию  риска(подготовка)
        con1 = {'type': 'eq', 'fun': constraint1}  # передача условий в функцию  риска(подготовка)
        con2 = {'type': 'ineq', 'fun': constraint2}  # передача условий в функцию  риска(подготовка)
        cons = [con1, con2]  # передача условий в функцию  риска(подготовка)
        sol = minimize(objective, x0, method='SLSQP', \
                       bounds=bnds, constraints=cons)

        status = sol.message
        weights = sol.x
        weights = [np.round(x, 7) for x in weights]
        weights = weights / np.sum(weights)
        return weights, status
