import unittest
import requests
import builtins
import cmd_line_parser as cml_parser

from unittest.mock import patch, Mock


class TestRSSReader(unittest.TestCase):
    """Tests functions from rss_reader.py"""

    def setUp(self):
        self.logger = Mock()
        self.command_line_args = Mock()

    @patch('logging.INFO', 'INFO')
    def test_output_verbose(self):

        self.command_line_args.verbose = False
        logger = cml_parser.output_verbose(self.command_line_args, self.logger)
        self.logger.info.assert_not_called()
        self.logger.setLevel.assert_not_called()
        self.assertEqual(logger, None)

        self.command_line_args.verbose = True
        logger = cml_parser.output_verbose(self.command_line_args, self.logger)
        self.logger.info.assert_called_with('Output info logs in console.')
        self.logger.setLevel.assert_called_with('INFO')
        self.assertEqual(logger, None)

    def test_output_version(self):

        self.command_line_args.version = True
        with patch('builtins.print'):
            cml_parser.output_version(self.command_line_args, self.logger)
            self.logger.info.assert_called_with('Output the RSS reader version')

        self.command_line_args.version = False
        self.assertIsNone(cml_parser.output_version(self.command_line_args, self.logger))


if __name__ == '__main__':
    unittest.main()
