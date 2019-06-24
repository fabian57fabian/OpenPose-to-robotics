import argparse


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="0",
                        help="Input source. Choose between: "
                             "\nA webcam e.g. '0' or IP path 'http://192.168.1.49:4141/video'"
                             "\nA video with relative path e.g. 'video.avi'."
                             "\n(Default: 0)")
    parser.add_argument("--disable-car", action="store_true", default=False,
                        help="Disable comunication to Car. (Default false)")
    parser.add_argument("--compute-analytics", action="store_true", default=False,
                        help="Compute analytics. (Default false)")
    parser.add_argument("--show-analytics", action="store_true", default=False,
                        help="Shows analytics after computation. (Default false)")
    parser.add_argument("--unoptimized-speed", action="store_true", default=False,
                        help="Disable speed optimization and error checking. (Default false)")
    parser.add_argument("--unoptimized-steer", action="store_true", default=False,
                        help="Disable steer optimization and error checking. (Default false)")
    args = parser.parse_args()
    _s = 0
    try:
        _s = int(args.source)
    except:
        _s = args.source
    return (not args.disable_car), _s, args
