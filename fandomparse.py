import requests
from bs4 import BeautifulSoup


class FandomParserException(Exception):
    pass


class FandomParser:
    _fandomUrl = "https://losyash-library.fandom.com/ru/wiki/"

    def __init__(self, episode_name):
        self._webpage_url = FandomParser._fandomUrl +\
                            FandomParser._prepare_episode_name(episode_name)

        request = requests.get(self._webpage_url)
        self._soup = BeautifulSoup(request.text, "lxml")

    def get_section_list(self, section_name):
        section_id = section_name.replace(" ", "_")
        section_span = self._soup.find("span", {"id": section_id})
        if section_span is None:
            raise FandomParserException("section '{}' not found".format(
                section_name))

        section_header = section_span.parent
        section_ul_list = section_header.next_sibling.next_sibling
        section_list = [element.text.strip() for element in
                        section_ul_list.find_all("li")
                        if element.text.strip() != ""]

        return section_list

    @staticmethod
    def _prepare_episode_name(episode_name):
        if episode_name[-2] == "-":
            episode_name = episode_name[:-2]

        return episode_name.replace(" ", "_")
