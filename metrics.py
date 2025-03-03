import itertools
import numpy as np


def calculate_mrd(pass_rates: list[float]) -> float:
    """计算最大角色差异 (MRD@k)"""
    if len(pass_rates) < 2:
        return 0.0

    max_diff = 0.0
    # 生成所有两两组合
    for a, b in itertools.combinations(pass_rates, 2):
        denominator = a + b
        if denominator == 0:
            current_diff = 0.0
        else:
            current_diff = abs(a - b) / denominator * 100
        max_diff = max(max_diff, current_diff)

    return max_diff


def calculate_rsd(pass_rates: list[float]) -> float:
    """计算角色标准差 (RSD@k)"""
    n = len(pass_rates)
    if n < 2:
        return 0.0

    # mean = sum(pass_rates) / n
    # sum_sq_diff = sum((x - mean) ** 2 for x in pass_rates)
    # rsd = (sum_sq_diff / (n - 1)) ** 0.5  # 样本标准差

    rsd = np.std(pass_rates, ddof=1)  # 使用 numpy 计算标准差

    return rsd

def calculate_mean(pass_rates: list[float]) -> float:
    """计算平均值"""
    n = len(pass_rates)
    if n < 1:
        return 0.0

    return np.mean(pass_rates)


# 示例使用
if __name__ == "__main__":
    test_cases = [
        [87.9,86.3,86.8]
    ]

    for pass_rates in test_cases:
        mrd = round(calculate_mrd(pass_rates), 2)
        rsd = round(calculate_rsd(pass_rates), 2)
        print(f"Input: {pass_rates}")
        print(f"MRD: {mrd}%")
        print(f"RSD: {rsd}\n")

        # print(round(calculate_mean(pass_rates), 2))
