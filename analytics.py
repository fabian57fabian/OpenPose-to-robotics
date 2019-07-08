import matplotlib.pyplot as plt
import numpy as np
import time
import os

main_folder = "Analytics/"
file_format_plt = 'png'
file_format_np = 'txt'
file_dpi = 300


def createFileName(folder, name):
    if not os.path.exists(folder):
        os.makedirs(folder)
    separator = "" if str.endswith(folder, '/') else '/'
    return folder + separator + name


def ProcessAnalytics(accelerations, no_opt_acc, steering_angles, no_opt_steer, fps_loss, args):
    if args.compute_analytics:
        name = time.strftime("%Y%m%d_%H%M%S")
        path = main_folder + name + "/"
        os.makedirs(path)
        ProcessSpeeds(accelerations, no_opt_acc, args.show_analytics, path, name)
        ProcessSteeringAngles(steering_angles, no_opt_steer, args.show_analytics, path, name)
        ProcessFpsLoss(fps_loss, args.show_analytics, path, name)


def ProcessFpsLoss(fps_loss, show, folder, name):
    plt.figure(3)
    x_data = np.arange(len(fps_loss))
    plt.scatter(x_data, fps_loss)
    plt.title("Fps loss")
    plt.xlabel("Step")
    plt.ylabel("Loss")
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    filename = createFileName(folder + "FpsLoss", name)
    plt.savefig(filename + "." + file_format_plt, format=file_format_plt, dpi=file_dpi)
    np.savetxt(createFileName(folder + "FpsLoss", "fps_loss_" + name) + "." + file_format_np, fps_loss, fmt='%.9f')
    if show:
        plt.show()


def ProcessSpeeds(accelerations, no_op, show, folder, name):
    plt.figure(1)
    plt.plot(no_op)
    plt.plot(accelerations)
    plt.title("Acceleration analytics")
    plt.xlabel("Step")
    plt.ylabel("Speed")
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    filename = createFileName(folder + "Speeds", name)
    plt.savefig(filename + "." + file_format_plt, format=file_format_plt, dpi=file_dpi)
    np.savetxt(createFileName(folder + "Speeds", "opt_" + name) + "." + file_format_np, accelerations, fmt='%d')
    np.savetxt(createFileName(folder + "Speeds", "nop_" + name) + "." + file_format_np, no_op, fmt='%d')
    if show:
        plt.show()


def ProcessSteeringAngles(steering_angles, no_op, show, folder, name):
    plt.figure(2)
    plt.plot(no_op)
    plt.plot(steering_angles)
    plt.title("Steering analytics")
    plt.xlabel("Step")
    plt.ylabel("Angle")
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    filename = createFileName(folder + "SteeringAngles", name)
    plt.savefig(filename + "." + file_format_plt, format=file_format_plt, dpi=file_dpi)
    np.savetxt(createFileName(folder + "SteeringAngles", "opt_" + name) + "." + file_format_np, steering_angles,
               fmt='%d')
    np.savetxt(createFileName(folder + "SteeringAngles", "nop_" + name) + "." + file_format_np, no_op, fmt='%d')
    if show:
        plt.show()
