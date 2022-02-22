from Environment import Environment
from Block import Block
from Autopoiesis import Autopoiesis
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import time

E = Environment(20,20,4,2)

"""
plt.ion()
fig, ax1 = plt.subplots()
data = np.zeros((10, 10))
h = sns.heatmap(data,ax=ax1,cbar=False,vmin=0, vmax=1)
ax1.invert_yaxis()
cb = h.figure.colorbar(h.collections[0])  # 显示colorbar
cb.ax.tick_params(labelsize=18)  # 设置colorbar刻度字体大小。
for i in range(10):
    ax1.cla()
    data = np.random.random((10, 10))
    h = sns.heatmap(data,ax=ax1,cbar=False)
    plt.pause(0.1)
plt.ioff()
plt.show()

"""