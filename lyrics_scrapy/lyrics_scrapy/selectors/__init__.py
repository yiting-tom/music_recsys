#%%
import pandas as pd
from ._base import BaseSelector


# %%
s = BaseSelector(
    raw_dir="../data/album-list/htm",
    rules={
        "artist": lambda sel: sel.xpath("//dd/h1//a[1]/@href").getall(),
        "album": lambda sel: sel.xpath("//dd/h1//a[2]/@href").getall(),
        "tracks": lambda sel: sel.xpath("//dd/div//a/@href").getall(),
    }
)

ans = s.select()
full = pd.concat(ans)

full.album.to_csv("../data/album-list/selected/album.csv", index=False)
full.to_csv("../data/album-list/selected/artist-album-list.csv", index=False)
full.to_pickle("../data/album-list/selected/artist-album-list.pkl")