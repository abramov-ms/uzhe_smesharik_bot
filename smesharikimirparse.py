import requests
from bs4 import BeautifulSoup


class SmesharikiMirException(Exception):
    pass


class SmesharikiMirParser:
    _websiteUrl = "https://smeshariki-mir.ru/"

    @staticmethod
    def _page_url(page_number):
        return EpisodeListParser._websiteUrl + "?page_id=" + \
               str(page_number)


class EpisodeListParser(SmesharikiMirParser):
    oldFlatEpisodeListPage = 12
    new3dEpisodesListPage = 4755

    def __init__(self, webpage_index):
        request = requests.get(SmesharikiMirParser._page_url(webpage_index))
        self._soup = BeautifulSoup(request.text, "lxml")
        self._episode_rows = self._soup.find_all(
            "tr",
            {"class": ["table-gr", "table-y", "table-g"], "valign": "top"})

    def get_episode_name(self, episode_number):
        episode_row = self._episode_rows[self._episode_index(episode_number)]
        first_column = episode_row.find("td", {"class": "text7"})
        episode_name = first_column.find_all(text=True)[1].strip()
        if episode_name.endswith("3D"):
            episode_name = episode_name[:-3]

        return episode_name

    def get_episode_description(self, episode_number):
        episode_row = self._episode_rows[self._episode_index(episode_number)]
        second_column = episode_row.find("td", {"class": "text5"})
        episode_description = second_column.find(text=True).strip()

        return episode_description

    def get_episode_video_page_index(self, episode_number):
        episode_row = self._episode_rows[self._episode_index(episode_number)]
        first_column = episode_row.find("td", {"class": "text7"})
        video_link = first_column.find("a")
        video_page_index = int(video_link.attrs["href"][9:])

        youtube_button_image = video_link.find("img")
        if youtube_button_image.attrs["src"].endswith("youtubebw.png"):
            raise SmesharikiMirException(
                "could not find video page for ep. #" + str(episode_number))

        return video_page_index

    def episodes_count(self):
        return len(self._episode_rows)

    def _episode_index(self, episode_number):
        if episode_number not in range(1, self.episodes_count() + 1):
            raise SmesharikiMirException("ep. number is out of range")

        return episode_number - 1


class VideoPageParser(SmesharikiMirParser):
    def __init__(self, webpage_index):
        request = requests.get(SmesharikiMirParser._page_url(webpage_index))
        self._soup = BeautifulSoup(request.text, "lxml")

    def get_video_link(self, timecode=0):
        video_url = self._soup.find("iframe").attrs["src"].strip()
        if "embed" in video_url and "youtube" in video_url:
            yt_video_id = video_url[30:-6]
            return "https://youtu.be/{}?t={}".format(yt_video_id, timecode)
        else:
            return video_url


oldEpisodesListParser = EpisodeListParser(
    EpisodeListParser.oldFlatEpisodeListPage)
newEpisodesListParser = EpisodeListParser(
    EpisodeListParser.new3dEpisodesListPage)
