#!/usr/bin/env python3.8

import feedparser
import html
import json
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from errors import InvalidURL


class RSSparser:
    """
    Parsed the RSS news from received link, extracts required amount of news and prints result
    in human readable format.

    Parameters:
        args: parsed given arguments out of sys.argv;
        logger: imported from logger module for tracking events that happen when program runs.

    Returns:
        store_news: list of dictionaries with extracted info of required amount of parsed news;
        output_txt_news method returns result in human readable format (filling the prepared).
    """

    def __init__(self, args, logger):
        self.url = args.source
        self.limit = args.limit
        self.logger = logger
        self.logger.info(f'Get RSS_url {self.url} and value = {self.limit} (limits amount of output news)')
        # convert string to the unicode
        self.text_updater = html.unescape
        self.response = self._parse_url(self.url)
        # Extract the news-site name
        self.feed_name = self.text_updater(self.response.feed.title)
        # Extract all news separately in one list
        self.logger.info('Separate a news from the URL.')
        self.news = self.response.entries
        self.amount_of_news = len(self.news)
        self.limit = self._check_limit_value(self.limit, self.amount_of_news)
        self.all_news = self._parse_feed()

    def _parse_url(self, url):
        """
        Check the URL is correct, get a response from the URL if the status code is 200
        :param url: user defined url
        :return: response from the valid url
        """
        try:
            response = feedparser.parse(url)
            self.logger.info(f'Getting the response from the URL: {url}.')
        except AttributeError:
            raise InvalidURL("Please, check the URL.")

        if response.status != 200:
            raise Exception(f'Bad response status code {str(response.status)}')

        return response

    def _check_limit_value(self, limit, total):
        """
        Check if received limit value is valid
        :param limit: user defined limit value from command line arguments
        :param total: total amount of news received from the site
        :return: valid value of limit variable
        """
        if limit and not 0 < limit <= total:
            self.logger.info(f'Check if the received limit value = {limit} is valid.')
            raise ValueError(f'Limit value is outside the valid range: from 1 to {total}.')
        elif not limit:
            limit = total
            self.logger.info(f"The 'limit' variable is assigned the total amount of received news {limit}.")
            return limit

        return limit

    def _parse_feed(self):
        """
        Parse set amount of news from URL and write required news to the list of dictionaries
        :return: list of dictionaries with appropriate info
        """
        img_link, img_title = None, None
        store_news = []

        self.logger.info('Extract the required data from the separated news '
                         'and fill the dictionaries with required data.')
        for info in self.news[:self.limit]:
            info_title = self.text_updater(info.title)
            info_link = info.link
            info_date = info.published
            info_description = info.description

            # Pulling data out of HTML part
            soup = BeautifulSoup(info_description, features="html.parser")

            if soup.img:
                img_link = soup.img['src']
                img_title = self.text_updater(soup.img['title'])

            info_text = self.text_updater(soup.text)

            store_news.append({
                "title": info_title,
                "link": info_link,
                "date": info_date,
                "img_title": img_title,
                "img_link": img_link,
                "text": info_text,
            })
        return store_news

    def output_txt_news(self):
        """
        Fill template with required data
        :return: print the completed template
        """
        self.logger.info('Load the template.')

        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('template.txt')

        self.logger.info('Fill the template with relevant data.')
        # Filling template with appropriate data
        output = template.render(feed_name=self.feed_name, all_news=self.all_news[:self.limit])

        print(output)
