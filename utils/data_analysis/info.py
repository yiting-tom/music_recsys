from typing import Callable

import pandas as pd
from tabulate import tabulate as tab


class Info:
    def __init__(self, df: pd.DataFrame, *, tablefmt: str = "psql") -> None:
        self.df = df
        self.cols = df.columns
        self.tablefmt = tablefmt
    
    def __show(fn: Callable) -> Callable:
        def wrap(self):
            print("="*20, fn.__name__, "="*20)
            fn(self)
            print()
        return wrap
    
    @__show
    def show_info(self) -> None:
        print(self.df.info())
    
    @__show
    def show_unique_info(self) -> None:
        print(tab(
            tabular_data=[[
                    col,
                    self.df[col].nunique(),
                    f"{self.df[col].nunique()/len(self.df)*100:.1f}%",
                ] for col in self.cols ],
            headers=["column", "#", "%"],
            tablefmt=self.tablefmt,
        ))

    @__show
    def show_nan_info(self) -> None:
        print(tab(
            tabular_data=[[
                    col,
                    self.df[col].isna().sum(),
                    f"{self.df[col].isna().sum()/len(self.df)*100:.1f}%",
                ] for col in self.cols ],
            headers=["column", "#", "%"],
            tablefmt=self.tablefmt,
        ))
        