import numpy as np
import pandas as pd

def calculate_psi(expected, actual, bins=5):
    e_percents = np.histogram(expected.dropna(), bins=bins)[0] / len(expected.dropna())
    a_percents = np.histogram(actual.dropna(), bins=bins)[0] / len(actual.dropna())
    e_percents = np.where(e_percents == 0, 1e-4, e_percents)
    a_percents = np.where(a_percents == 0, 1e-4, a_percents)
    return float(np.sum((a_percents - e_percents) * np.log(a_percents / e_percents)))

if __name__ == "__main__":
    train_df = pd.read_csv("data/train.csv")
    test_df = pd.read_csv("data/test.csv")
    features = ["Online boarding", "Inflight wifi service", "Seat comfort", "Departure Delay in Minutes"]
    print("=== Feature Drift Audit (Population Stability Index) ===")
    for feat in features:
        psi = calculate_psi(train_df[feat], test_df[feat])
        status = "STABLE (<0.10)" if psi < 0.10 else "MODERATE DRIFT (0.10-0.25)"
        print(f"{feat:<30} | PSI = {psi:.4f} | {status}")