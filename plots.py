import numpy as np
import matplotlib.pyplot as plt

for i in range(20):
    N = 5
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([3, 4, 5, 2, i])
    colors = np.array(['black']*5)
    #area = (30 * np.random.rand(N))**2  # 0 to 15 point radii
    area = 4

    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    saveloc = 'plots/scatter' + str(i) + '.png'
    plt.savefig(saveloc)
    plt.close()