#%%
from pathlib import Path
import re
from typing import Tuple
import scrapy
from scrapy.http import Response
from ..settings import DATA_DIR

def get_all_artists(filepath: Path) -> Tuple[str]:
    """get_all_artists function
    
    Returns a list of all artists in the given filepath.
    
    Args:
        filepath (Path): The filepath.
    
    Returns:
        List[str]: The artists.
    """
    with open(filepath, 'r') as f:
        for line in f.readlines():
            if line not in (DATA_DIR / "htm/artist/").glob("*.htm"):
                yield ('https://mojim.com' + line.strip())


class ArtistSpider(scrapy.Spider):
    name = 'artist'
    allowed_domains = ['mojim.com']
    start_urls = get_all_artists(DATA_DIR / "csv/artist-id.csv")
    re_filename = re.compile(r'(?<=.com\/)[\w.]+')
    save_path = DATA_DIR / "htm/artist/"
    save_path.mkdir(exist_ok=True, parents=True)

    def parse(self, res: Response):
        page = res.xpath(r'//*[@id="inS"]/dl').get()
        filename = self.re_filename.search(res.url).group(0)
        with open(DATA_DIR / f"htm/artist/{filename}", 'w+') as f:
            f.write(page + '\n')
#%%
DATA_DIR = Path(__file__).parent.parent / "data"
len(list(get_all_artists(DATA_DIR / "csv/artist-id.csv")))