from ._base import BaseSelector
import pandas as pd

def main():
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

    for column in full.columns:
        pd.Series(full[column], name=column) \
            .to_csv(f"../data/csv/{column}.csv", index=False)