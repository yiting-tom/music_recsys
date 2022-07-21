from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, TypeVar, Union


@dataclass
class DatasetConfig:
    # The root directory of all the datasets.
    ROOT_DIR: Path = Path(__file__).parent.parent.parent / "datasets"

    # The state of the dataset for choosing.
    STATES = TypeVar(
        "STATES",
        bound=Literal["raw", "processed", "ready"]
    )
