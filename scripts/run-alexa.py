from __future__ import print_function

import argparse
import json
import sys
sys.path.append('../src/main/python')

from alexa import lambda_handler


def parse_args():
    parser = argparse.ArgumentParser(description="Runs mylawn")
    parser.add_argument('--file', '-f', type=str, metavar='FILE', help="The sample json file to read")
    return parser.parse_args()


if __name__ == '__main__':
    arguments = parse_args()

    json_file = arguments.file
    print("Using file: " + str(json_file))

    with open(json_file) as data_file:
        data = json.load(data_file)
        print("Response:\n" + json.dumps(lambda_handler(data, None), sort_keys=True, indent=4))
