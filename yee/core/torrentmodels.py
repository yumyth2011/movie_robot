import datetime
import hashlib
from enum import Enum
from typing import List

ListStr = List[str]
ListInt = List[int]


class TorrentType(str, Enum):
    Movie = '电影'
    Series = '剧集'
    Music = '音乐'
    AV = '成人'
    Other = '其他'

    @staticmethod
    def get_type(type: str):
        for item in TorrentType:
            if item.name == type:
                return item
        return None


class Series(object):
    season_start: int = None
    season_end: int = None
    season_full_index: ListInt = []
    ep_start: int = None
    ep_end: int = None
    ep_full_index: ListInt = []
    ep_is_fill = False


class Torrent(object):
    id: int = None
    site_name: str = None
    site: str = None
    url: str = None
    name: str = None
    subject: str = None
    movies_release_year: str = None
    type: TorrentType = None
    media_source: str = None
    media_encoding: str = None
    primitive_type: str = None
    cate: str = None
    file_size: int = 0
    upload_count: int = 0
    download_count: int = 0
    publish_time: datetime = None
    red_seed: bool = False
    free_deadline: datetime = datetime.datetime.min
    series: Series = None
    score = None

    @property
    def hash_id(self):
        hashlib.sha256(self.url.encode('utf-8')).hexdigest()

    def to_json(self):
        return {
            'id': self.id,
            'site_name': self.site_name,
            'site': self.site,
            'url': self.url,
            'name': self.name,
            'subject': self.subject,
            'movies_release_year': self.movies_release_year,
            'primitive_type': self.primitive_type,
            'type': self.type.name,
            'media_source': self.media_source,
            'media_encoding': self.media_encoding,
            'cate': self.cate,
            'file_size': self.file_size,
            'upload_count': self.upload_count,
            'download_count': self.download_count,
            'publish_time': self.publish_time,
            'red_seed': self.red_seed,
            'free_deadline': self.free_deadline.strftime('%Y-%m-%d %H:%m:%s')
        }


Torrents = List[Torrent]


class FileTorrent(object):
    url: str
    name: str
    filepath: str

    def to_json(self):
        return {
            'url': self.url,
            'name': self.name,
            'filepath': self.filepath
        }
