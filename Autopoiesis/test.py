import numpy as np
import matplotlib.pyplot as plt
data = np.load("myfile.npy")
plt.figure(dpi=300,figsize=(8,6))
plt.plot(list(range(len(data[0:500]))),data[0:500])
plt.grid()
plt.title("Integrity of Autopoiesis",fontsize=14)
plt.xlabel("Time")
plt.ylabel("Integrity")
plt.savefig("0-25.jpg")
plt.show()



