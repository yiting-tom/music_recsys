#%%
import re
from pathlib import Path
from typing import Iterable, List, Tuple

import scrapy
from scrapy.http import Response

from ..settings import DATA_DIR


def get_all_urls(start: Tuple[int, int], end: Tuple[int, int]) -> Iterable[str]:
    """get_all_urls function
    
    Returns a list of all URLs for the given start and end (year, month).

    Args:
        start (Tuple[int, int]): The start year and month.
        end (Tuple[int, int]): The end year and month.

    Yields:
        Generator[str]: The URLs.
    """
    for year in range(start[0], end[0] + 1):
        for month in range(1, 13):
            # Skip the month if it is not in the range
            if year == start[0] and month < start[1] \
            or year == end[0] and month > end[1]:
                continue
            yield f"https://mojim.com/uszlist{year}-{month:02d}.htm"

class AlbumListSpider(scrapy.Spider):
    name = 'album-list'
    allowed_domains = ['mojim.com']
    start_urls = get_all_urls((2000, 1), (2022, 7))
    re_year_mon = re.compile(r'(\d{4})-(\d{2})')
    save_dir: Path = DATA_DIR / 'htm/timeline/'
    save_dir.mkdir(exist_ok=True, parents=True)

    def parse(self, res: Response):
        year_mon: str = self.re_year_mon.search(res.url).group(0)
        albums: List[str] = res.xpath(r'//div[@id="inS"]//dd').getall()

        filepath: Path = (self.save_dir / year_mon).with_suffix('.htm')
        with open(filepath, 'w+') as f:
            f.write('\n'.join(albums))
