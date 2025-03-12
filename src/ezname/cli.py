import argparse

from ezname.core import generate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix", type=str, default=None)
    parser.add_argument("-s", "--suffix", type=str, default=None)
    parser.add_argument("-d", "--delimiter", type=str, default="-")
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    print(generate(args.prefix, args.suffix, args.delimiter))
