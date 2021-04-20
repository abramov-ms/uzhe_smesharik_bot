import unittest
from unittest.mock import MagicMock

import requests
from bs4 import BeautifulSoup

from fandomparse import FandomParser, FandomParserException


class Object:
    pass


class MyTestCase(unittest.TestCase):
    def setUp(self):
        request = Object()
        with open("resources/fandomparse_test_page.html", "r") as page:
            request.text = page.read()

        requests.get = MagicMock(return_value=request)
        self.parser = FandomParser("Скамейка")

    def test_soup(self):
        requests.get.assert_called_once_with(
            "https://losyash-library.fandom.com/ru/wiki/Скамейка")

        with open("resources/fandomparse_test_page.html", "r") as page:
            expected_soup = BeautifulSoup(page.read(), "lxml")
            self.assertEqual(expected_soup, self.parser._soup)

    def test_get_non_existing_section(self):
        with self.assertRaises(FandomParserException):
            self.parser.get_section_list("Несуществующий раздел")

    def test_get_section_without_lists(self):
        self.assertEqual([], self.parser.get_section_list("Сюжет"))

    def test_get_section_with_list(self):
        self.assertEqual(5, len(self.parser.get_section_list("Персонажи")))
        self.assertEqual(7, len(self.parser.get_section_list("Ляпы")))
        self.assertEqual(
            7, len(self.parser.get_section_list("Интересные факты")))

    def test_prepare_episode_name(self):
        self.assertEqual(
            FandomParser._prepare_episode_name("Рок-опера и что-то ещё"),
            "Рок-опера_и_что-то_ещё")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
