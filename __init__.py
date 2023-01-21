import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.interpolate import make_interp_spline


# 定义每一个人当前的进度范围
class User:
    def __init__(self, start, end, loc, target):
        self.start = start
        self.end = end
        self.loc = loc

        # 初始化单次进度向量
        # 由于卷积默认从0开始，所以先初始化一个end+1的向量矩阵
        length = end - start + 1
        self.vec = np.zeros(end + 1)
        for ii in range(start, end + 1):
            self.vec[ii] = 1.0 / length

        # 计算需要的最少回合数与最大回合数
        self.distance = target - loc
        self.fast = math.ceil(self.distance / end)
        self.low = math.ceil(self.distance / start)

    def get_times_vec(self):
        count = 0
        array_mat = self.vec

        count_array = np.zeros(self.low)

        while count < self.low:
            array_mat = add_by_convolution(array_mat, self.vec)
            # 当大于fast时，开始执行操作
            if count >= self.fast:
                # 计算当前概率
                count_array[count] = np.sum(array_mat[self.distance:array_mat.shape[0]])
            count = count + 1

        return count_array


def add_by_convolution(x, y):
    return fftconvolve(x, y)


def reset_vec(x):
    temp = np.zeros(x.shape[0])
    for ii in range(1, x.shape[0]):
        temp[ii] = x[ii] - x[ii - 1]
    return temp


def plot_by_spline(vec, str_info):
    x_label = np.linspace(0, vec.shape[0], 1000)
    x_ori = np.arange(vec.shape[0])
    model = make_interp_spline(x_ori, vec)
    new_y_a = model(x_label)
    plt.plot(x_label, new_y_a, label=str_info)


if __name__ == '__main__':
    # 定义最后需要到达的数字
    target_number = int(input('输入总进度'))
    start_x = int(input('当前进度'))
    start_y = int(input('竞争对手进度'))
    a_1 = int(input('您的最低进度'))
    a_2 = int(input('您的最高进度'))
    b_1 = int(input('竞争对手的最低进度'))
    b_2 = int(input('竞争对手的最高进度'))

    a = User(a_1, a_2, start_x, target_number)
    b = User(b_1, b_2, start_y, target_number)
    vec_a = reset_vec(a.get_times_vec())
    vec_b = reset_vec(b.get_times_vec())

    plot_by_spline(vec_a, 'Distribution of your time')
    plot_by_spline(vec_b, 'Distribution of opponent\'s time')

    plt.legend()
    plt.savefig('时间分布图像.png')

    sum_rate = 0
    for i in range(vec_a.shape[0]):
        for j in range(vec_b.shape[0]):
            if i <= j:
                sum_rate = sum_rate + vec_a[i] * vec_b[j]
    print("最后一天先于竞争对手的胜率", sum_rate)
    sum_rate = 0
    for i in range(vec_a.shape[0]):
        for j in range(vec_b.shape[0]):
            if i < j:
                sum_rate = sum_rate + vec_a[i] * vec_b[j]
    print("最后一天晚于竞争对手的胜率", sum_rate)

    x=input('点击回车键退出')
