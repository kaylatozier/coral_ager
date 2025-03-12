#!/usr/bin/env python

"""
Command line interface to darwin_day
"""

import argparse
from darwinday import birthday, info


def parse_command_line():
    "parses args for the darwin_day funtion"

    # init parser and add arguments
    parser = argparse.ArgumentParser()

    # add long args
    parser.add_argument(
        "--next",
        help="returns a countdown until the next Darwin Day",
        action="store_true")

    # add long args
    parser.add_argument(
        "--last",
        help="returns a countdown since the last Darwin Day",
        action="store_true")

    parser.add_argument(
        "--info",
        help="returns a random fact about Chuck D.",
        action="store_true")

    # parse args
    args = parser.parse_args()

    # check that user only entered one action arg
    if sum([args.next, args.last, args.info]) > 1:
        raise SystemExit(
            "only one of 'next', 'last' or 'info' at a time.")
    return args


def main():
    "run main function on parsed args"

    # get arguments from command line as a dict-like object
    args = parse_command_line()

    # pass argument to call darwinday function
    if args.next:
        birthday('next')
    elif args.last:
        birthday('last')
    elif args.info:
        info()


if __name__ == "__main__":
    birthday('next')
    info()
