import datetime
import re


class PTSiteParser:
    @staticmethod
    def get_free_deadline(freetime: str) -> datetime:
        t = re.match(r'(?:(\d+)日)?(?:(\d+)[時时])?(?:(\d+)分)?', freetime)
        if not t:
            return None
        now = datetime.datetime.now()
        if t.group(1):
            now = now + datetime.timedelta(days=int(t.group(1)))
        if t.group(2):
            now = now + datetime.timedelta(hours=int(t.group(2)))
        if t.group(3):
            now = now + datetime.timedelta(minutes=int(t.group(3)))
        return now

    @staticmethod
    def trans_unit_to_mb(size: float, unit: str) -> float:
        if unit == 'GB' or unit == 'GiB':
            return round(size * 1024, 2)
        elif unit == 'MB' or unit == 'MiB':
            return round(size, 2)
        elif unit == 'KB' or unit == 'KiB':
            return round(size / 1024, 2)
        elif unit == 'TB' or unit == 'TiB':
            return round(size * 1024 * 1024, 2)
