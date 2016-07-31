from __future__ import print_function
from __future__ import print_function
import argparse
from mylawn.mylawn import get_water_info
from mylawn.alexa import lambda_handler
from config.settings import WUNDERGROUND_STATION


def parse_args():
    parser = argparse.ArgumentParser(description="Runs mylawn")
    parser.add_argument('--alexify', '-a', dest='alexify', action='store_true', default=False,
                        help="Alexify the output")
    parser.add_argument('--station', '-s', type=str, metavar='ID', default=WUNDERGROUND_STATION,
                        help="The weather underground station to use")
    return parser.parse_args()


if __name__ == '__main__':
    arguments = parse_args()

    # print(arguments)

    if arguments.alexify:
        # print(lambda_handler(None, None))
        print(lambda_handler(None, None))
    else:
        print("".join(get_water_info(arguments.station)))
