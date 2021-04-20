from pyyoutube import Api


class FirstResultSearcher:
    _api = Api(api_key="AIzaSyBWyP2NFMJd6v24FPnf4g1ghDnpcRogeF4")
    _videoUrl = "https://youtu.be/{}?t={}"

    def get_youtube_video_url(self, query, timecode=0):
        youtube_search = FirstResultSearcher._api.search_by_keywords(
            q=query, search_type=["video"], count=1, limit=1)

        return self._videoUrl.format(youtube_search.items[0].id.videoId,
                                     timecode)


searcher = FirstResultSearcher()
