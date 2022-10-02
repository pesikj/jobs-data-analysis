import numpy as np
import matplotlib.pyplot as plt

x = ["A", "B"]
y_bot = [10, 20]
y_dif = [100, 30]

plt.xlim(-5, 200)

plt.barh(x, left=y_bot, width=y_dif)

plt.show()

