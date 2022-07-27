#%%
from pathlib import Path
import re
from typing import Tuple
import scrapy
from scrapy.http import Response
from ..settings import DATA_DIR

def get_all_artists(artist_id_path: Path, processed_path: Path) -> Tuple[str]:
    """get_all_artists function
    
    Returns a list of all artists in the given filepath.
    
    Args:
        filepath (Path): The filepath.
    
    Returns:
        List[str]: The artists.
    """
    processed_fname = {out.name for out in processed_path.glob("*.htm")}

    with open(artist_id_path, 'r') as f:
        all_artist_ids = {line.strip()[1:] for line in f.readlines()}

    for fname in all_artist_ids.difference(processed_fname):
        yield f"https://mojim.com/{fname}"


class ArtistSpider(scrapy.Spider):
    name = 'artist'
    allowed_domains = ['mojim.com']
    save_path = DATA_DIR / "htm/artist/"
    start_urls = get_all_artists(
        artist_id_path = DATA_DIR / "csv/artist-id.csv",
        processed_path = save_path,
    )
    re_filename = re.compile(r'(?<=.com\/)[\w.]+')
    save_path.mkdir(exist_ok=True, parents=True)

    def parse(self, res: Response):
        # get the target element.
        page = res.xpath(r'//*[@id="inS"]/dl').get()
        # get filename from the url.
        filename = self.re_filename.search(res.url).group(0)
        # save the htm to the file.
        with open(DATA_DIR / f"htm/artist/{filename}", 'w+') as f:
            f.write(page + '\n')