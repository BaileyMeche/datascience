"""
Thank you to Tobias Rodriguez del Pozo for his assistance in writing this code.
"""

import numpy as np
import pandas as pd

import misc_tools
import pull_CRSP_stock
from settings import config

OUTPUT_DIR = config("OUTPUT_DIR")
DATA_DIR = config("DATA_DIR")

def calc_equal_weighted_index(df):
    """
    Calculate equal weighted index (just the average of all stocks)
    Note that ret is raw and retx is adjusted for dividends.
    """
    # Group by date and compute the average returns and count the number of securities.
    df_eq_idx = df.groupby("date").agg({
        "ret": "mean",
        "retx": "mean",
        "permno": "count"
    })
    df_eq_idx = df_eq_idx.rename(
        columns={
            "ret": "ewretd",
            "retx": "ewretx",
            "permno": "totcnt",
        }
    )
    # Ensure the index name is "date" (as expected by the tests)
    df_eq_idx.index.name = "date"
    df_eq_idx = df_eq_idx.dropna(how="all")
    return df_eq_idx


def calc_CRSP_value_weighted_index(df, freq="MS"):
    """
    The formula is:
    $$
    r_t = \frac{\sum_{i=1}^{N_t} w_{i,t-1} r_{i,t}}{\sum_{i=1}^{N_t} w_{i,t-1}}
    $$
    That is, the return of the index is the weighted average of the returns, where
    the weights are the market cap of the stock at the end of the previous month.
    """
    _df = df.copy()
    _df["mktcap"] = _df["shrout"] * _df["altprc"]

    # Create lagged market cap column.
    # Note: misc_tools.with_lagged_columns returns a column named "L1_mktcap".
    _df = misc_tools.with_lagged_columns(
        df=_df,
        column_to_lag="mktcap",
        id_column="permno",
        date_col="date",
        lags=1,
        freq=freq,
    )
    # Group by date and compute the weighted average returns using the lagged market cap.
    grouped = _df.groupby("date")
    ret = grouped.apply(lambda g: np.sum(g["ret"] * g["L1_mktcap"]) / np.sum(g["L1_mktcap"]))
    retx = grouped.apply(lambda g: np.sum(g["retx"] * g["L1_mktcap"]) / np.sum(g["L1_mktcap"]))
    mkt_cap = grouped["mktcap"].sum()

    df_vw_idx = pd.concat(
        {
            "vwretd": ret,
            "vwretx": retx,
            "totval": mkt_cap,
        },
        axis=1,
    )
    # Set the first (earliest) row to NaN (since there is no lagged data) then drop such rows.
    df_vw_idx.iloc[0, :] = np.nan
    df_vw_idx = df_vw_idx.dropna(how="all")
    return df_vw_idx

def calc_CRSP_indices_merge(df_msf, df_msix, freq="ME"):
    # Merge everything with appropriate suffixes
    df_vw_idx = calc_CRSP_value_weighted_index(df_msf, freq=freq)
    df_eq_idx = calc_equal_weighted_index(df_msf)
    df_msix = df_msix.rename(columns={"caldt": "date"})

    df = df_msix.merge(
        df_vw_idx.reset_index(),
        on="date",
        how="inner",
        suffixes=("", "_manual"),
    )
    df = df.merge(
        df_eq_idx.reset_index(),
        on="date",
        suffixes=("", "_manual"),
    )
    df = df.set_index("date")
    return df

def _demo():
    df_msf = pull_CRSP_stock.load_CRSP_monthly_file(data_dir=DATA_DIR)
    df_msix = pull_CRSP_stock.load_CRSP_index_files(data_dir=DATA_DIR)

    df_eq_idx = calc_equal_weighted_index(df_msf)
    df_vw_idx = calc_CRSP_value_weighted_index(df_msf, freq="ME")
    df_idxs = calc_CRSP_indices_merge(df_msf, df_msix, freq="ME")
    df_idxs.head()


if __name__ == "__main__":
    pass
