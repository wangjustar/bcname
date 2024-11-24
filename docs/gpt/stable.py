import numpy as np
import matplotlib.pyplot as plt

# 常量
a = 100
b = 2
c = 2010


# 函数定义
def activity(expenditure, income, registration_time, reputation):
    term1 = (expenditure / (income + a))
    term2 = np.maximum(registration_time - c, 0) / 10
    term3 = (reputation / 100) ** b
    return (term1 + term2) * term3


# 创建数据
expenditure_income = np.linspace(0, 10000, 100)
registration_time = np.linspace(2000, 2024, 100)
reputation = np.linspace(0, 100, 100)
expenditure_multiple = np.linspace(0, 2, 100)
income = 10  # 假设收入为5000

if __name__ == "__main__":
    # 支出/收入图
    plt.figure(figsize=(10, 5))
    plt.plot(expenditure_income, activity( 5000,expenditure_income, 2015, 50),
             label='Income=5000, Registration=2015, Reputation=50')
    plt.xlabel('Expenditure/Income')
    plt.ylabel('Activity')
    plt.title('Activity vs Expenditure/Income')
    plt.legend()
    plt.grid(True)
    plt.show()
    #
    # # 注册时间图
    # plt.figure(figsize=(10, 5))
    # plt.plot(registration_time, activity(5000, 5000, registration_time, 50),
    #          label='Income=5000, Registration=2015, Reputation=50')
    # plt.xlabel('Registration Time')
    # plt.ylabel('Activity')
    # plt.title('Activity vs Registration Time')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    #
    # # 信誉值图
    # plt.figure(figsize=(10, 5))
    # plt.plot(reputation, activity(5000, 5000, 2015, reputation),
    #          label='Income=5000, Registration=2015, Reputation=Variable')
    # plt.xlabel('Reputation')
    # plt.ylabel('Activity')
    # plt.title('Activity vs Reputation')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # # 支出倍数图
    # plt.figure(figsize=(30, 5))
    # plt.plot(expenditure_multiple, activity(expenditure_multiple*income, income, 2015, 100))
    # plt.xlabel('Expenditure Multiple')
    # plt.ylabel('Activity')
    # plt.title('Activity vs Expenditure Multiple')
    # plt.grid(True)
    # plt.show()
