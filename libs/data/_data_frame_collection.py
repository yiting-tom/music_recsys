from pathlib import Path
from typing import Any, Generator, List, Literal, Optional

import pandas as pd
from libs.data.config import DatasetConfig as DC


class DataFrameCollection:
    """DataFrameCollection class

    Args:
        name (str): Name of the dataset.
        dfs (Optional[List[str]], optional): Names of picked data frames. Defaults to None (all data frames in folder).
        state (Optional[DC.STATES], optional): State of data. Defaults to "raw".
    """
    def __init__(
        self,
        name: str,
        dfs: Optional[List[str]] = None,
        state: Optional[DC.STATES] = "raw",
    ):
        self.name: str = name
        self.state: str = state
        self.dir: Path = DC.ROOT_DIR / name / state
        self.dfs: List[str] = dfs or []

        self.set_all_dfs(ftype="pkl")

    def set_all_dfs(self, ftype: Literal["plk", "csv"] = "pkl") -> None:
        """set_all_dfs method
        
        Set all DataFrames with specific suffix into attributes.

        Args:
            ftype (str, optional): The file type of data frames. Defaults to "pkl".
        
        Raises:
            ValueError: If the file type is not "pkl" or "csv" or no data frames fount.
        """
        # Update the folder path with file type.
        self.dir = self.dir / ftype
        print(f"reading DataFrames from {self.dir}")

        # Get all the files in the directory.
        all_dfs: Generator[Path] = self.dir.glob("*." + ftype)

        # Check if the data frames are exist.
        if all_dfs is None and self.dfs is None:
            raise ValueError(f"No data frames found in {self.dir}.")

        # If the list of dfs is not given, we use all the files.
        for df_name in self.dfs or all_dfs:
            # Get the file path.
            df_path: Path = self.dir / df_name
            # Set suffix for the path.
            location: Path = df_path.with_suffix(f".{ftype}")
            # Read the data frame from the path.
            df: pd.DataFrame = pd.read_pickle(location) \
                if ftype == "pkl" \
                else pd.read_csv(location)

            setattr(self, df_path.stem, df)
            self.dfs.append(df_path.stem)
    
    def add_df(self, name: str, df: pd.DataFrame) -> None:
        """add_df method
        
        Add a data frame to the collection.
        
        Args:
            name (str): Name of the data frame.
            df (pd.DataFrame): Data frame to be added.
        """
        setattr(self, name, df)
        self.dfs.append(name)
    
    def save_dfs(self, ftype: Literal["plk", "csv"] = "pkl") -> None:
        """save_dfs method
        
        Save all data frames in the collection.
        
        Args:
            ftype (str, optional): The file type of data frames. Defaults to "pkl".
        """
        # Update the folder path with file type.
        self.dir = self.dir / ftype
        print(f"saving DataFrames to {self.dir}")
        # Save all data frames.
        for df_name in self.dfs:
            # Get the file path.
            df_path: Path = self.dir / df_name
            # Set suffix for the path.
            location: Path = df_path.with_suffix(f".{ftype}")
            # Save the data frame to the path.
            getattr(self, df_name).to_pickle(location)
    
    def __repr__(self) -> str:
        return f"<DataFrameCollection {self.name}>"
        
