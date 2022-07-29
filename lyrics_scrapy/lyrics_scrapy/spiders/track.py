#%%
from pathlib import Path
import re
from typing import Tuple
import scrapy
from scrapy.http import Response
from ..settings import DATA_DIR
import scrapy

def get_all_tracks(track_id_path: Path, processed_path: Path) -> Tuple[str]:
    """get_all_tracks function
    
    Returns a list of all tracks in the given filepath.
    
    Args:
        filepath (Path): The filepath.
    
    Returns:
        List[str]: The tracks.
    """
    processed_fname = {out.name for out in processed_path.glob("*.htm")}

    with open(track_id_path, 'r') as f:
        all_track_ids = {line.strip()[1:] for line in f.readlines()}

    for fname in all_track_ids.difference(processed_fname):
        yield f"https://mojim.com/{fname}"

class TrackSpider(scrapy.Spider):
    name = 'track'
    allowed_domains = ['mojim.com']
    save_path = DATA_DIR / "htm/track/"
    start_urls = list(get_all_tracks(
        track_id_path = DATA_DIR / "csv/track-id.csv",
        processed_path = save_path,
    ))[:150000]
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