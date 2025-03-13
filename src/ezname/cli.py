import argparse

from ezname.core import generate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix", type=str, default=None)
    parser.add_argument("-s", "--suffix", type=str, default=None)
    parser.add_argument("-d", "--delimiter", type=str, default="-")
    parser.add_argument("-n", "--num", type=int, default=1)
    args = parser.parse_args()

    for _ in range(args.num):
        print(
            generate(prefix=args.prefix, suffix=args.suffix, delimiter=args.delimiter)
        )
