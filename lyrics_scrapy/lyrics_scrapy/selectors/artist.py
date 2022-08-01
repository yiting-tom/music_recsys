from ._base import BaseSelector
import pandas as pd
from settings import DATA_DIR

def main():
    s = BaseSelector(
        raw_dir=DATA_DIR / "htm/artist",
        rules={
            "artist_name": lambda sel: sel.xpath(r'//*[@id="Tb3"]/div[1]/span[3]/a/span/text()').get(),
            "artist_type": lambda sel: sel.xpath(r'//*[@id="Tb3"]/div[1]/span[2]/a/span/text()').get(),
            "artist_intro": lambda sel: sel.xpath(r'//div[@id="inS"]/dl/dd[@class="hb0"]').get(),
        }
    )
    all_dfs = pd.concat(s.select(id_name="artist_id"))
    ordered_dfs = all_dfs[['artist_id', 'artist_name', 'artist_type', 'artist_intro']]
    ordered_dfs.to_csv(DATA_DIR / "csv/artist.csv", index=False)