#!/bin/env python3
import argparse
import logging
import sys

from bankii.processor import Processor

logger = logging.getLogger()


def setup_logger():
    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main(args):
    setup_logger()
    p = Processor()
    p.initialize()
    p.process(args.source, args.destination, args.output_format, args.output_file)
    p.finalize()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Converts bank statements to standard output format'
    )
    parser.add_argument('-s', '--source', type=str,
                        help="Source folder containing bank statements in formats. Eg: xls, csv files", required=True)
    parser.add_argument('-d', '--destination', type=str,
                        help="Destination folder for output file", required=True)

    parser.add_argument('-o', '--output-format', type=str,
                        help="Output file format", default="csv", choices=['csv'])
    parser.add_argument('-f', '--output-file', type=str,
                        help="Output file", default='output')

    args = parser.parse_args()
    main(args)
