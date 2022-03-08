import cgi
import datetime
import io
import logging
import os
import re
import time
import zipfile
from urllib.parse import unquote

from yee.core.httputils import RequestUtils
from yee.core.torrentmodels import Torrents, FileTorrent, Torrent, TorrentType
from yee.pt.ptsite import PTSite


class Jackett(PTSite):
    def split(text, delimiter='/'):
        if text is None or len(text) == 0:
            return []
        return text.split(delimiter)

    def login(self):
        try:
            res = self.req.get(
                url='%s/api/v2.0/indexers?apikey=%s&configured=true&_=%s' % (
                    self.get_site(), self.kwargs['api_key'], int(time.time())),
                headers=self.headers,
                skip_check=True
            ).json()
            if len(res) > 0:
                sites = []
                for item in res:
                    sites.append(item['name'])
                logging.info('jackett: %s连接成功，已配置 %d 个站点：[%s]' % (self.get_site(), len(sites),'；'.join(sites)))
        except Exception as e:
                logging.error('jackett: %s连接失败，请检查 地址 和 api_key' % self.get_site())


    def login_by_cookie(self, cookie: str):
        pass

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    req = RequestUtils(request_interval_mode=True)

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if kwargs['address'] is None or kwargs['api_key'] is None:
            raise RuntimeError('必须指定jackett的服务地址和api_key，缺一不可')
        else:
            self.login()

    def get_site(self):
        """
        返回pt站的网址
        :return:
        """
        return self.kwargs['address']

    def get_site_name(self):
        """
        这是pt网站的名称，确保唯一即可，集成到主程序时用作配置项
        :return:
        """
        return 'jackett'

    def get_torrent_list(self, url, result_page_limit=5) -> Torrents:
        return []

    def search_torrent(self, keyword, result_page_limit=5, use_imdb_search: bool = False) -> Torrents:
        return self.automatic_page_loading(
            '%s/api/v2.0/indexers/all/results?apikey=%s&Query=%s&_=%s' % (
                self.get_site(), self.kwargs['api_key'], keyword, int(time.time()))
        )

    def automatic_page_loading(self, url) -> Torrents:
        search_result = []
        res = self.req.get(
            url=url,
            headers=self.headers,
            skip_check=True
        )
        if res is None:
            return search_result
        result = res.json()
        if 'Results' in result.keys() and len(result['Results']) > 0:
            search_result = self.parse_torrents(result['Results'])
        return search_result

    def parse_torrents(self, result) -> Torrents:
        search_result = []
        for r in result:
            t = Torrent()
            t.site_name = self.get_site_name()
            t.site = self.get_site()
            types = Jackett.split(r['CategoryDesc'], '/')
            t.primitive_type = types[0]
            if t.primitive_type == 'Movies':
                t.type = TorrentType.Movie
                t.cate = TorrentType.Movie.value
            elif t.primitive_type == 'TV':
                t.type = TorrentType.Series
                t.cate = TorrentType.Series.value
            elif t.primitive_type == 'Audio':
                t.type = TorrentType.Music
                t.cate = TorrentType.Music.value
            else:
                t.type = TorrentType.Other
                t.cate = r['CategoryDesc']
            t.name = r['Title']
            t.subject = r['Description']
            t.url = r['Link']
            # t.movies_release_year = mp.parse_year_by_str_list([t.name, t.subject])
            id_match = re.findall(r'id=(\d+)', r['Guid'])
            if id_match is not None and len(id_match) > 0:
                t.id = id_match[0]
            else:
                t.id = int(time.time())
            t.upload_count = r['Seeders']
            t.download_count = r['Grabs']
            t.red_seed = r['Seeders'] == 0
            # t.publish_time = datetime.datetime.now()
            try:
                if r['PublishDate'] is not None:
                    dateMatch = re.findall(
                        r'(\d{4}-\d{2}-\d{2}).*(\d{2}:\d{2}:\d{2}).*?([\+\-]\d{2}:\d{2})?$', r['PublishDate'])
                    if len(dateMatch) > 0:
                        timedelta = datetime.timedelta()
                        if dateMatch[0][2] != '':
                            timedelta = datetime.timedelta(hours=8) - datetime.datetime.strptime(dateMatch[0][2].replace(':', ''),'%z').utcoffset()
                        t.publish_time = datetime.datetime.strptime(
                            dateMatch[0][0] + ' ' + dateMatch[0][1], '%Y-%m-%d %H:%M:%S') + timedelta
                    else:
                        logging.error('未识别jackett时间格式：%s' % r['PublishDate'])
            except Exception as e:
                logging.error('未识别jackett时间格式：%s' % r['PublishDate'])
            t.file_size = round(r['Size'] / 1024 / 1024, 2)
            if r['DownloadVolumeFactor'] == 0:
                t.free_deadline = datetime.datetime.max
            search_result.append(t)
        return search_result

    def parse_download_filename(self, response):
        if 'Content-Disposition' not in response.headers:
            print(response.headers)
            return None
        value, params = cgi.parse_header(unquote(response.headers['Content-Disposition']))
        return params['filename']

    def download_torrent(self, url, save_dir) -> FileTorrent:
        r = self.req.get(url, headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }, allow_redirects=True, skip_check=True)
        if r.status_code != 200 and r.status_code != 302:
            logging.info('种子下载失败(%s)：%s' % (r.status_code, url))
            return None
        ft = FileTorrent()
        filename = self.parse_download_filename(r)
        if filename is None:
            logging.info('无法下载种子：%s' + url)
            return None
        ft.url = r.url
        ft.name = os.path.splitext(filename)[0]
        if os.path.splitext(filename)[-1] == '.zip':
            torrent_filename = None
            zfile = zipfile.ZipFile(io.BytesIO(r.content))
            for item in zfile.namelist():
                cn_name = item.encode('cp437').decode('gbk')
                if os.path.splitext(item)[-1] == '.torrent':
                    torrent_filename = cn_name
                    zfile.extract(item, save_dir + os.sep)
                    os.rename(save_dir + os.sep + item, save_dir + os.sep + cn_name)
            zfile.close()
            if torrent_filename is None:
                logging.info('错误的种子zip压缩包，请人工检查确认%s' % filename)
                return None
            else:
                ft.filepath = save_dir + os.sep + torrent_filename
        else:
            ft.filepath = save_dir + os.sep + filename
            with open(ft.filepath, 'wb') as f:
                f.write(r.content)
        return ft
