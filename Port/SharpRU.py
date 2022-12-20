import numpy as np
import random
import Port.sharp_derivative as functions_2

class SharpPortfolio:

    def __init__(self, returns, cov_mat, args=None, riskless_ret=((1 + 0.03)**(1/252) - 1)):
        self.returns = returns
        self.cov_mat = cov_mat
        self.riskless_ret = riskless_ret

    def fit(self, step=0.0015):
        random.seed(10)

        # ОПГ
        lr = 0.1
        num_of_iter = 100
        grad_weights = np.array([1 / len(self.returns)] * len(self.returns))
        weights_history = np.empty(num_of_iter, dtype=object)


        # MOMENTUM
        for _ in range(num_of_iter):
            function_value, gradient = functions_2.fAndG(
                self.cov_mat, self.returns, self.riskless_ret, grad_weights)
            weights_history[_] = grad_weights
            grad_weights = 2 * grad_weights - lr * gradient
            ret_loc, risk_loc = self.get_risk_ret(grad_weights)

        grad_weights = np.clip(grad_weights, 0, np.inf)
        grad_weights = grad_weights / np.sum(grad_weights)
        status = True
        return grad_weights, status

    def get_risk_ret(self, weights):
        weights = weights.reshape(-1, 1)
        returns = self.returns.reshape(-1, 1)

        return_port = weights.T @ returns
        risk_port = np.sqrt(weights.T @ self.cov_mat @ weights)
        return [float(return_port), float(risk_port)]