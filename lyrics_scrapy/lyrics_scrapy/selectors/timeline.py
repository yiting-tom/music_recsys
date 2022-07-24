#%%
import pandas as pd
#%%
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

full.artist.unique().to_csv("../data/csv/artist-id.csv", index=False)
full.album.unique().to_csv("../data/csv/album-id.csv", index=False)
full.tracks.unique().to_csv("../data/csv/track-id.csv", index=False)