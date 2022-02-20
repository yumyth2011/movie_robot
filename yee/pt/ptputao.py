import cgi
import datetime
import re
from urllib.parse import unquote

from yee.core.torrentmodels import Torrents, TorrentType, Torrent
from yee.pt.nexusprogramsite import NexusProgramSite
from yee.pt.ptsiteparser import PTSiteParser


class PTPuTao(NexusProgramSite):
    def get_site(self):
        """
        返回pt站的网址
        :return:
        """
        return 'https://pt.sjtu.edu.cn'

    def get_site_name(self):
        """
        这是pt网站的名称，确保唯一即可，集成到主程序时用作配置项
        :return:
        """
        return 'putao'

    def parse_torrents(self, text: str) -> Torrents:
        """
        通过返回的网页代码，解析列表页种子的所有信息
        :param text:
        :return:
        """
        type_list = re.findall(
            r'<td class=rowfollow .+ style=.+><span class=.+><a href=".*cat=\d+" title="([^"]+)"><img .+ src=".+" alt="([^"]+)" ></a></span></td>',
            text)
        search_result = []
        for type in type_list:
            t = Torrent()
            t.site_name = self.get_site_name()
            t.site = self.get_site()
            t.primitive_type = type[0]
            if "电影" in t.primitive_type:
                t.type = TorrentType.Movie
                t.cate = TorrentType.Movie.value
            elif "电视剧" in t.primitive_type:
                t.type = TorrentType.Series
                t.cate = TorrentType.Series.value
            elif "音乐" in t.primitive_type:
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
            r'''<a title="([^"]+)"\s+href="details.php\?id=(\d+).*?<br />(.*?)</td>''',
                text)):
            t = search_result[i]
            t.name = r[0]
            t.id = r[1]
            t.subject = r[2]
            t.url = self.get_site() + '/download.php?id=' + t.id
            # 这里需要去解析种子中的剧集年份，可以留空，集成到主框架时，我可以改这个细节
            # t.movies_release_year = mp.parse_year_by_str_list([t.name, t.subject])
            # 匹配种子发布时间、文件大小、大小单位、做种数量,是否红种、下载数量
        for i, r in enumerate(re.findall(
            r'''<span class='nobr' title='([^']+)'>.*?<td class=rowfollow>([0123456789\.]+)<br/>(TB|GB|MB|KB)</td><td class=rowfollow.*?>(?:<b><a href=.*toseeders=1><font color=>(.+)</font></a></b>)?(?:<span class="red">(.+)</span>)?</td>\n?.*?\n?.*?viewsnatches.*?<b>(.+)</b>''',
                text)):
            t = search_result[i]
            t.publish_time = datetime.datetime.strptime(r[0], '%Y-%m-%d %H:%M:%S')
            t.file_size = PTSiteParser.trans_unit_to_mb(float(r[1]), r[2])
            if r[3] != '':
                t.upload_count = int(r[3].replace(',', ''))
            else:
                t.upload_count = int(r[4].replace(',', '')) if r[4] != '' else 0
                t.red_seed = True
            t.download_count = int(r[5].replace(',', '')) if r[5] != '' else 0
        return search_result

    def parse_download_filename(self, response):
        if 'Content-Disposition' not in response.headers:
            print(response.headers)
            return None
        value, params = cgi.parse_header(unquote(response.headers['Content-Disposition']))
        return params['filename']
