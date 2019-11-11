#!/usr/bin/env python3.8

import os
import sys
import json
import logging
import argparse

from logger import logger


# Make a parser for parsing exact arguments out of sys.argv.
parser = argparse.ArgumentParser(description="Performs a variety of operations on a file.")

parser.add_argument('source', help='RSS URL')
parser.add_argument('--version', action="store_true", help="Print version info")
parser.add_argument('--json', action="store_true", help="Print result as JSON in stdout")
parser.add_argument('--verbose', action="store_true", help="Outputs verbose status messages")
parser.add_argument('--limit', type=int, default=None, help="Limit news topics if this parameter provided")


def output_json(news_parser, arguments, logger):
    """
    While the 'json' argument was passed - converts data in json format and prints it
    """
    if arguments.json:
        logger.info('Output result of parsing RSS in JSON format')
        news_in_json = json.dumps(news_parser.all_news)
        print(news_in_json)


def output_verbose(arguments, logger):
    """
    While the 'verbose' argument was passed, func reports events that occur during normal operation of a program
    """
    if arguments.verbose:
        logger.info('Output info logs in console.')
        logger.setLevel(logging.INFO)


def output_version(arguments, logger):
    """
    While the 'version' argument was passed - prints the program version
    """
    if arguments.version:
        logger.info('Output the RSS reader version')
        print("RSS_reader 1.0")