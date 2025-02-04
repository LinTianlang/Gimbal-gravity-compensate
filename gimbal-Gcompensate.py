from sympy import symbols, sin, cos, pi
from sympy import solve, Eq
import numpy as np
import math
# task1:计算弹簧-连杆连接点的坐标

# 定义所有符号变量（包括自变量和因变量）
L1, L2, theta_pitch = symbols('L1 L2 theta_pitch')  # 自变量L1为弹簧-云台耳轴架连接点在电机-云台耳轴连线（向量OD）上相对于云台耳轴转点的距离，L2为弹簧-连杆转点相对于连杆上转点的距离，theta_pitch为云台俯仰角
xc, yc = symbols('xc yc')  # 因变量为弹簧-连杆转点（C点）的坐标

# 定义已知量
L1 = 0.05235  # 以L1=0.05235为例，计算xc和yc的值
L2 = 0.02  # 以L2=0.1为例，计算xc和yc的值
L3 = 0.03  # 摇臂长度，以L3=0.03为例，计算xc和yc的值
K = 550  # 弹簧刚度系数
L0 = 0.02  # 弹簧自然长度
theta_pitch = 30 * 0.01745  # theta_pitch是云台俯仰角

vec_OA = np.array([-L3*math.cos(theta_pitch), -L3*math.sin(theta_pitch)])  # 向量AO的坐标
vec_OB = np.array([L1*math.cos(76.96*pi/180), -L1*math.sin(76.96*pi/180)])  # 向量OB的坐标

# 定义方程组
eq1 = Eq((xc + L3*cos(theta_pitch))*(-0.05235*sin(76.96*0.01745)), (yc - L3*sin(theta_pitch))*0.05235*cos(76.96*0.01745)) #pitch连杆（向量AC）与电机-云台耳轴连线（向量OD）平行
eq2 = Eq(L2 ** 2,(xc + L3*cos(theta_pitch)) ** 2 + (yc - L3*sin(theta_pitch)) ** 2) #弹簧-连杆转点（C点）在连杆上且与连杆上转点（A点）距离为L2（即模长为L2）

# 解方程组，明确指定因变量xc和yc为未知数
solutions = solve([eq1, eq2], [xc, yc])

#计算点C和各个向量的坐标
xc = solutions[1][0]
yc = solutions[0][1]*-1
vec_OC = np.array([xc, yc])  # 向量BC的坐标
vec_BC = vec_OC - vec_OB  # 向量BC的坐标
vec_CA = vec_OA - vec_OC # 向量AC的坐标

# 输出task1结果：
print(f"云台俯仰角={theta_pitch/0.01745}° 时：")
# print(f"s1 = {solutions[0]}, s2 = {solutions[1]}") # 输出完整解，用于验证算法正确性
# print(f"x_c = {solutions[1][0]}, y_c = {solutions[0][1]*-1}")

# 输出各个向量的坐标
# print(f"vec_OA = {vec_OA}")
# print(f"vec_OB = {vec_OB}")
# print(f"vec_OC = {vec_OC}")
# print(f"vec_BC = {vec_BC}")
# print(f"vec_CA = {vec_CA}")

# task2:计算向量BC的模长
norm_BC = vec_BC.dot(vec_BC) ** 0.5
print(f"向量BC的模长(弹簧长度)为{norm_BC}米")
# task3:计算向量AC和向量BC的夹角、向量OA和向量AC的夹角
norm_CA = vec_CA.dot(vec_CA) ** 0.5
norm_OA = vec_OA.dot(vec_OA) ** 0.5
cos_theta = vec_CA.dot(vec_BC) / (norm_CA * norm_BC)
cos_alpha = vec_OA.dot(vec_CA) / (norm_OA * norm_CA)
theta = math.acos(cos_theta)
alpha = math.acos(cos_alpha)
print(f"连杆和弹簧的夹角为{theta/0.01745}度")
print(f"连杆和从动摇臂的夹角为{alpha/0.01745}度")
# task4:计算作用于pitch轴从动摇臂的切向力
F = K * (norm_BC - L0)
F1 = F * math.cos(theta)
Ft = F1 * math.sin(alpha)
print(f"弹簧的拉力为{F}牛顿")
print(f"作用于pitch轴从动摇臂的切向力为{Ft}牛顿")
# task5:计算机构实际产生的补偿力矩
T_compensate = Ft * L3
print(f"弹簧的刚度系数为{K}牛/米，自然长度为{L0}米")
print(f"机构实际产生的补偿力矩为{T_compensate}牛米")

# 找到了一个可以很方便地计算实际拉簧被拉伸时的拉力的网站：https://zxspring.net/fuwu/springlali.html
# 可以用来边翻手册边验证计算结果。当然，理论计算和实际计算的结果可能会有一些误差。
