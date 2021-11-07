"""Matrix Constructor for Stock
"""
from tqdm import tqdm
import pandas as pd
from .base import MatrixConstructor


class StockMatrixConstructor(MatrixConstructor):
    """Construct Correlation Matrix for Stock Data"""

    implemented_options = ["price", "volume"]

    def __init__(self, option, **configs):
        super().__init__(**configs)
        self.option = option

    def get_matrix(self, df):
        quarters = df.quarter.unique()
        df["Date"] = pd.to_datetime(df["Date"])
        companies = [list(com.keys())[0] for com in self.companies]
        res = {
            quarter: pd.DataFrame(0, index=companies, columns=companies)
            for quarter in quarters
        }
        if self.option == "price":
            agg_val = "Close"
        elif self.option == "volume":
            agg_val = "Volume"
        else:
            raise NotImplementedError(
                f"please specify option in {self.implemented_options}"
            )
        for quarter in tqdm(quarters):
            quarter_df = df[df.quarter == quarter]
            res[quarter] = quarter_df.pivot_table(
                index="Date", columns="ticker_symbol", values=agg_val
            ).corr()
        for quarter, mat in res.items():
            res[quarter] = mat.values
        return res