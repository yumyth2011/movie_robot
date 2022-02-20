import cgi
import datetime
import re
from urllib.parse import unquote

from yee.core.torrentmodels import Torrents, TorrentType, Torrent
from yee.pt.nexusprogramsite import NexusProgramSite
from yee.pt.ptsiteparser import PTSiteParser


class PTKeepfrds(NexusProgramSite):
    def get_site(self):
        """
        返回pt站的网址
        :return:
        """
        return 'https://pt.keepfrds.com'

    def get_site_name(self):
        """
        这是pt网站的名称，确保唯一即可，集成到主程序时用作配置项
        :return:
        """
        return 'keepfrds'

    def parse_torrents(self, text: str) -> Torrents:
        """
        通过返回的网页代码，解析列表页种子的所有信息
        :param text:
        :return:
        """
        type_list = re.findall(
            r'<td class="rowfollow nowrap".+><a\s+href=".*cat=\d+"><img class=".+" src="/static/pic/cattrans.gif" alt="([^"]+)"\s*(?:title="[^"]+")?\s*style=".+"\s*/></a>',
            text)
        search_result = []
        for type in type_list:
            t = Torrent()
            t.site_name = self.get_site_name()
            t.site = self.get_site()
            t.primitive_type = type
            if t.primitive_type in ['电影', '电影(合集)']:
                t.type = TorrentType.Movie
                t.cate = TorrentType.Movie.value
            elif t.primitive_type in ['剧集', '剧集(合集)']:
                t.type = TorrentType.Series
                t.cate = TorrentType.Series.value
            elif t.primitive_type in ['音乐', '音乐(合集)', '音乐录影带(合集)', '音乐录影带(合集)']:
                t.type = TorrentType.Music
                t.cate = TorrentType.Music.value
            elif t.primitive_type in ['纪录片', '纪录片(合集)']:
                t.type = TorrentType.Other
                t.cate = '纪录片'
            elif t.primitive_type in ['综艺', '综艺(合集)']:
                t.type = TorrentType.Other
                t.cate = '综艺'
            elif t.primitive_type in ['体育', '体育(合集)']:
                t.type = TorrentType.Other
                t.cate = '体育'
            elif t.primitive_type in ['动漫', '动漫(合集)']:
                t.type = TorrentType.Other
                t.cate = '动漫'
            else:
                t.type = TorrentType.Other
                t.cate = TorrentType.Other.value
            search_result.append(t)
        for i, r in enumerate(re.findall(
                r'<a title="([^"]+)"\s+href=".*?id=(\d+).*?<br />(?:<font.*?>)?([^<]*)(?:.*alt="([^"]*Free)".*title=&quot;(.*?)&quot;.*)?.*?rowfollow nowrap">(.*?)<br\s*/>(.*?)</td>.*?rowfollow">(.*?)<br\s*/>(.*?)</td>(?:.*class="(red)">(\d+).*)?(?:.*seeders">(\d+).*?)?\n?(?:.*viewsnatches.*?<b>(\d+).*?)?',
                text)):
            t = search_result[i]
            t.subject = r[0]
            t.id = r[1]
            t.url = self.get_site() + '/download.php?id=' + r[1]
            t.name = r[2]
            if r[3] != '':
                if r[4] != '':
                    t.free_deadline = datetime.datetime.strptime(r[4], '%Y-%m-%d %H:%M:%S')
                else:
                    t.free_deadline = datetime.datetime.max
            # 这里需要去解析种子中的剧集年份，可以留空，集成到主框架时，我可以改这个细节
            # t.movies_release_year = mp.parse_year_by_str_list([t.name, t.subject])
            # 匹配种子发布时间、文件大小、大小单位、做种数量,是否红种、下载数量
            t.publish_time = datetime.datetime.strptime(r[5] + ' ' + r[6], '%Y-%m-%d %H:%M:%S')
            t.file_size = PTSiteParser.trans_unit_to_mb(float(r[7]), r[8])
            if r[9] == 'red':
                t.red_seed = True
                t.upload_count = int(r[10])
            else:
                t.upload_count = int(r[11])
            t.download_count = int(r[12]) if r[12] != '' else 0
        return search_result

    def parse_download_filename(self, response):
        if 'Content-Disposition' not in response.headers:
            print(response.headers)
            return None
        value, params = cgi.parse_header(unquote(response.headers['Content-Disposition']))
        return params['filename']
