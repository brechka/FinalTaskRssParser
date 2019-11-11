#!/usr/bin/env python3.8

from cmd_line_parser import parser, output_verbose, output_json, output_version
from rss_parser import RSSparser
from logger import logger


def main():
    # parse arguments received from the command line
    command_line_args = parser.parse_args()
    output_verbose(command_line_args, logger)

    rss_parser = RSSparser(command_line_args, logger)
    if not command_line_args.json:
        rss_parser.output_txt_news()
    output_json(rss_parser, command_line_args, logger)
    output_version(command_line_args, logger)


if __name__ == "__main__":
    main()

