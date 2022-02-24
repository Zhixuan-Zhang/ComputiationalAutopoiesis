import numpy as np
import matplotlib.pyplot as plt
data = np.load("myfile.npy")
plt.plot(list(range(len(data))),data)
plt.grid()
plt.title("Integrity of Autopoiesis")
plt.xlabel("Time")
plt.ylabel("Integrity")
plt.show()


