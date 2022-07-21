from pathlib import Path
from typing import Any, Callable, Generator, List, Literal, Optional

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
        self.dfs: List[str] = dfs or []

        self.set_all_dfs(ftype="pkl")
    
    @property
    def dir(self) -> Path:
        return DC.ROOT_DIR / self.name / self.state
    
    def set_all_dfs(self, ftype: Literal["plk", "csv"] = "pkl") -> None:
        """set_all_dfs method
        
        Set all DataFrames with specific suffix into attributes.

        Args:
            ftype (str, optional): The file type of data frames. Defaults to "pkl".
        
        Raises:
            ValueError: If the file type is not "pkl" or "csv" or no data frames fount.
        """
        # Update the folder path with file type.
        folder: Path = self.dir / ftype
        print(f"reading DataFrames from {folder}")

        # Get all the files in the directory.
        all_dfs: Generator[Path] = folder.glob("*." + ftype)

        # If the list of dfs is not given, we use all the files.
        for df_name in all_dfs:
            # Get the file path.
            df_path: Path = folder / df_name
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
    
    def save_dfs(
        self,
        columns: List[str] = None,
    ) -> None:
        """save_dfs method
        
        Save all data frames in the collection by pickle.
        
        Args:
            columns (List[str], optional): DataFrames to be saved. Defaults to None (all columns).
        """
        # Update the folder path with file type.
        folder: Path = self.dir / "pkl"
        print(f"saving DataFrames {columns or self.dfs} to {folder}")

        # Save all data frames.
        for df_name in (columns or self.dfs):
            # Get the file path.
            df_path: Path = folder / df_name
            # Set suffix for the path.
            location: Path = df_path.with_suffix(".pkl")
            # Pickle the data frame to the path.
            getattr(self, df_name).to_pickle(location)
    
    def __repr__(self) -> str:
        return f"<DataFrameCollection {self.dir}>"
        
