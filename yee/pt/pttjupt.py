import cgi
import datetime
import re
from urllib.parse import unquote

from yee.core.torrentmodels import Torrents, TorrentType, Torrent
from yee.pt.nexusprogramsite import NexusProgramSite
from yee.pt.ptsiteparser import PTSiteParser


class PTtjupt(NexusProgramSite):
    def get_site(self):
        """
        返回pt站的网址
        :return:
        """
        return 'https://tjupt.org'

    def get_site_name(self):
        """
        这是pt网站的名称，确保唯一即可，集成到主程序时用作配置项
        :return:
        """
        return 'tjupt'

    def parse_torrents(self, text: str) -> Torrents:
        """
        通过返回的网页代码，解析列表页种子的所有信息
        :param text:
        :return:
        """
        type_list = re.findall(
            r'<td class="rowfollow nowrap".+><a href=".*cat=\d+"><img class=".+" src="pic/cattrans.gif" alt="([^"]+)"\s*(?:title="[^"]+")?\s*style=".+"\s*/></a>(?:<img.+alt="([^"]+)"\s*(?:title=".+"\s*)?/>)?',
            text)
        search_result = []
        for type in type_list:
            t = Torrent()
            t.site_name = self.get_site_name()
            t.site = self.get_site()
            t.primitive_type = type[0]
            if t.primitive_type == '电影':
                t.type = TorrentType.Movie
                t.cate = TorrentType.Movie.value
            elif t.primitive_type in ['剧集', '综艺']:
                t.type = TorrentType.Series
                t.cate = TorrentType.Series.value
            elif t.primitive_type == '音乐':
                t.type = TorrentType.Music
                t.cate = TorrentType.Music.value
            elif t.primitive_type == '纪录片':
                t.type = TorrentType.Other
                t.cate = '纪录片'
            elif t.primitive_type == '动漫':
                t.type = TorrentType.Other
                t.cate = '动漫'
            else:
                t.type = TorrentType.Other
                t.cate = TorrentType.Other.value
            search_result.append(t)
        for i, r in enumerate(re.findall(
                r'<td class="rowfollow.+".+>.+table class="torrentname".+<b>(.+)</b></a>(?:<br\s*/>(.+))?.*</td><td width.+<a href="(download.php\?id=(\d+))">',
                text)):
            t = search_result[i]
            t.name = r[0]
            t.subject = r[1]
            t.url = self.get_site() + '/' + r[2]
            # 这里需要去解析种子中的剧集年份，可以留空，集成到主框架时，我可以改这个细节
            # t.movies_release_year = mp.parse_year_by_str_list([t.name, t.subject])
            t.id = r[3]
            # 匹配种子发布时间、文件大小、大小单位、做种数量,是否红种、下载数量
        for i, r in enumerate(re.findall(
                r'<td.+><span\s+title="(.+)">.+</span></td><td.+>([0123456789\.]+)<br\s+/>(TiB|GiB|MiB|KiB)</td><td.+>(?:<b><a\s+href=".+seeders">)?(?:<font.+>)?([0123456789,]+)(</font>|</span>)?.+\s*.+\s*<td class="rowfollow">(?:<a\s*href="viewsnatches.php[^"]+"\s*target.+><b>)?([0123456789,]+)(?:</b>)?',
                text)):
            t = search_result[i]
            t.publish_time = datetime.datetime.strptime(r[0], '%Y-%m-%d %H:%M:%S')
            t.file_size = PTSiteParser.trans_unit_to_mb(float(r[1]), r[2])
            t.upload_count = int(r[3].replace(',', ''))
            if r[4] != '':
                t.red_seed = True
            t.download_count = int(r[5].replace(',', ''))
        return search_result

    def parse_download_filename(self, response):
        if 'Content-Disposition' not in response.headers:
            print(response.headers)
            return None
        value, params = cgi.parse_header(unquote(response.headers['Content-Disposition']))
        return params['filename']
