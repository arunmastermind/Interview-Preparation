from scipy.optimize import minimize

def objective(x):
    return (x[0] - 3) ** 2 + (x[1] + 1) ** 2

result = minimize(objective, x0=[0, 0])
print(result.x)