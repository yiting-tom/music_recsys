#%%
from pathlib import Path
import re
from typing import Tuple
import scrapy
from scrapy.http import Response
from ..settings import DATA_DIR
import scrapy


def get_all_albums(album_id_path: Path, processed_path: Path) -> Tuple[str]:
    """get_all_albums function
    
    Returns a list of all albums in the given filepath.
    
    Args:
        filepath (Path): The filepath.
    
    Returns:
        List[str]: The albums.
    """
    processed_fname = {out.name for out in processed_path.glob("*.htm")}

    with open(album_id_path, 'r') as f:
        all_album_ids = {line.strip()[1:] for line in f.readlines()}

    for fname in all_album_ids.difference(processed_fname):
        yield f"https://mojim.com/{fname}"

class AlbumSpider(scrapy.Spider):
    name = 'album'
    allowed_domains = ['mojim.com']
    save_path = DATA_DIR / "htm/album/"
    start_urls = get_all_albums(
        album_id_path = DATA_DIR / "csv/album-id.csv",
        processed_path = save_path,
    )
    re_filename = re.compile(r'(?<=.com\/)[\w.]+')
    save_path.mkdir(exist_ok=True, parents=True)

    def parse(self, res: Response):
        # get the target element.
        page = res.xpath(r'//*[@id="Tb3"]').get()
        # get filename from the url.
        filename = self.re_filename.search(res.url).group(0)
        # save the htm to the file.
        with open(self.save_path / filename, 'w+') as f:
            f.write(page + '\n')

# %%
DATA_DIR = Path(__file__).parent.parent / "data"
album_id_path = DATA_DIR / "csv/album-id.csv"
albums = list(get_all_albums(
    album_id_path=album_id_path,
    processed_path=DATA_DIR / "htm/album/",
))