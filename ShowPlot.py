import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


def main():
    main_dir = "Analytics/"
    dirs = os.listdir(main_dir)
    while True:
        test_name = choose_dir(dirs)
        _plot(main_dir + test_name + "/Speeds/", test_name)
        _plot(main_dir + test_name + "/SteeringAngles/", test_name)
        # _plotFps(main_dir + test_name + "/FpsLoss/", test_name)


def _plot(folder, name):
    plt.figure()
    data = np.loadtxt(folder + "opt_" + name + ".txt", dtype=float).ravel()
    data_nop = np.loadtxt(folder + "nop_" + name + ".txt", dtype=float).ravel()
    plt.plot(data_nop)
    plt.plot(data)
    plt.title(name + " analytics")
    plt.xlabel("Step")
    plt.ylabel("Data")
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    plt.show()


def _plotFps(folder, name):
    plt.figure()
    filename = folder + "fps_loss_" + name + ".txt"
    data = np.loadtxt(filename, dtype=float).ravel()
    x_data = np.arange(len(data))
    plt.scatter(x_data, data)
    plt.title(name + " analytics")
    plt.xlabel("Step")
    plt.ylabel("Fps loss")
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    plt.show()


def choose_dir(dirs):
    exit = False
    selected_index = 0
    while not exit:
        for i, dd in enumerate(dirs):
            print(str(i) + ": " + dd)
        number = input("Choose the timestamp of test (type number): ")
        try:
            selected_index = int(number)
            if 0 <= selected_index < len(dirs):
                exit = True
        except ValueError:
            pass
    return dirs[selected_index]


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
