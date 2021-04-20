import unittest
from unittest.mock import MagicMock

import requests
from bs4 import BeautifulSoup

from smesharikimirparse import SmesharikiMirParser, EpisodeListParser, \
    VideoPageParser, SmesharikiMirException


class Object:
    pass


class SmesharikiMirParserTestCase(unittest.TestCase):
    def test_page_url(self):
        self.assertEqual("https://smeshariki-mir.ru/?page_id=12",
                         SmesharikiMirParser._page_url(12))

    def tearDown(self):
        pass


class EpisodeListParserTest(unittest.TestCase):
    def setUp(self):
        request = Object()
        with open("resources/smesharikimir_test_page.html", "r") as page:
            request.text = page.read()

        requests.get = MagicMock(return_value=request)
        self.parser = EpisodeListParser(
            EpisodeListParser.oldFlatEpisodeListPage)

    def test_soup(self):
        requests.get.assert_called_once_with(
            "https://smeshariki-mir.ru/?page_id=12")

        with open("resources/smesharikimir_test_page.html", "r") as page:
            expected_soup = BeautifulSoup(page.read(), "lxml")
            self.assertEqual(expected_soup, self.parser._soup)

            expected_episode_rows = expected_soup.find_all(
                "tr",
                {"class": ["table-gr", "table-y", "table-g"], "valign": "top"})
            self.assertEqual(expected_episode_rows, self.parser._episode_rows)

    def test_episodes_count(self):
        self.assertEqual(71, self.parser.episodes_count())

    def test_episode_indexing(self):
        self.assertEqual("Пощады не будет", self.parser.get_episode_name(3))
        self.assertEqual(
            "Таланты и поклонница", self.parser.get_episode_name(71))
        self.assertEqual("Ничейный выигрыш", self.parser.get_episode_name(9))

    def test_get_episode_name(self):
        self.assertEqual("Иллюзионист", self.parser.get_episode_name(7))
        self.assertEqual("Власть моды", self.parser.get_episode_name(1))

    def test_get_episode_description(self):
        self.assertEqual("Барашу никак не получается получить внимание "
                         "Нюши, он хочет ей доказать свою безупречность и "
                         "обращается за помощью к Кар-Карычу….",
                         self.parser.get_episode_description(8))

    def test_get_episode_video_page_index(self):
        self.assertEqual(4699, self.parser.get_episode_video_page_index(7))
        self.assertEqual(2886, self.parser.get_episode_video_page_index(2))

    def test_episode_index(self):
        with self.assertRaises(SmesharikiMirException):
            self.parser._episode_index(0)
        with self.assertRaises(SmesharikiMirException):
            self.parser._episode_index(72)
        self.assertEqual(0, self.parser._episode_index(1))

    def tearDown(self):
        pass


class VideoPageParseTest(unittest.TestCase):
    def setUp(self):
        request = Object()
        with open("resources/video_page.html", "r") as page:
            request.text = page.read()

        requests.get = MagicMock(return_value=request)
        self.parser = VideoPageParser(4699)

    def test_soup(self):
        requests.get.assert_called_once_with(
            "https://smeshariki-mir.ru/?page_id=4699")

        with open("resources/video_page.html", "r") as page:
            expected_soup = BeautifulSoup(page.read(), "lxml")
            self.assertEqual(expected_soup, self.parser._soup)

    def test_get_video_link(self):
        self.assertEqual("https://youtu.be/U4-XswGeY8E?t=21",
                         self.parser.get_video_link(21))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
