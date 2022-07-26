#%%
from tqdm import tqdm
import pandas as pd
from pathlib import Path
from typing import Callable, Dict, Iterable, Union
from scrapy.selector import Selector

class BaseSelector:
    """BaseSelector 

    Args:
        raw_dir (Union[str, Path]): The raw directory.
        rules (Dict[str, Callable[[str], str]]): The rules.
        selected_dir (Optional[Union[str, Path]], optional): The processed data store directory. Defaults to None.
    """
    def __init__(
        self,
        raw_dir: Union[str, Path],
        rules: Dict[str, Callable[[str], str]],
    ):
        self.raw_dir = Path(raw_dir)
        self.rules = rules
    
    def select(self) -> Iterable[pd.DataFrame]:
        """select method
        
        Do the selection and return the selected data by each xpath.

        Yields:
            Iterator[Iterable[str]]: The selected data.
        """
        for filepath in tqdm(
            iterable=self.raw_dir.glob("*.*"),
            total=len(list(self.raw_dir.glob("*.*")))):

            # Read htm file.
            with open(filepath, 'r') as f:
                html: str = f.read()

            # Wrapper the html with Selector.
            sel: Selector = Selector(text=html)

            # Get the selected data.
            df = pd.DataFrame(
                processor(sel)
                for _, processor in self.rules.items()
            ).T
            df.columns = self.rules.keys()

            yield df