import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--source", default="",
                    help="Source file where numpy array is saved")
args = parser.parse_args()

if not os.path.exists(args.source):
    print("File " + args.source + " doesn't exist!")
    sys.exit(-1)

data = np.fromfile(args.source, dtype=float)
data1 = data.ravel()

plt.figure()
plt.plot(data1)
plt.title(args.source + " analytics")
plt.xlabel("Step")
plt.ylabel("Data")
figManager = plt.get_current_fig_manager()
figManager.full_screen_toggle()
plt.show()
