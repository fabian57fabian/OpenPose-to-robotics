import matplotlib.pyplot as plt
import numpy as np
import time
import os

main_folder = "Analytics/"
file_format = 'png'
file_dpi = 300
name_acceleration = 'Speeds'
name_steering_angle = 'Steerings'


def createFileName(folder, name):
    if not os.path.exists(folder):
        os.makedirs(folder)
    separator = "" if str.endswith(folder, '/') else '/'
    return folder + separator + name + time.strftime("_%Y%m%d_%H%M%S")


def ProcessAnalytics(accelerations, steering_angles, args):
    if args.compute_analytics:
        ProcessSpeeds(accelerations, args.show_analytics)
        ProcessSteeringAngles(steering_angles, args.show_analytics)


def ProcessSpeeds(accelerations, show):
    plt.figure(1)
    plt.plot(accelerations)
    plt.title("Acceleration analytics")
    plt.xlabel("Step")
    plt.ylabel("Speed")
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    filename = createFileName(main_folder + "Speeds", name_acceleration)
    plt.savefig(filename + "." + file_format, format=file_format, dpi=file_dpi)
    np.savetxt(filename + ".txt", accelerations)
    if show:
        plt.show()


def ProcessSteeringAngles(steering_angles, show):
    plt.figure(2)
    plt.plot(steering_angles)
    plt.title("Steering analytics")
    plt.xlabel("Step")
    plt.ylabel("Angle")
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    filename = createFileName(main_folder + "SteeringAngles", name_steering_angle)
    plt.savefig(filename + "." + file_format, format=file_format, dpi=file_dpi)
    np.savetxt(filename + ".txt", steering_angles)
    if show:
        plt.show()
