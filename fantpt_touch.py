import pandas as pd


def _apply_zscore(x: pd.Series, stat_dict: dict):
    position = x["FantPos"]
    fantpt_touch = x["FantPt/Touch"]

    stats = stat_dict.get(position)

    if not stats:
        return

    return (fantpt_touch - stats["mean"]) / stats["std"]


def apply_fantpt_touch_stats(pp_df: pd.DataFrame = None) -> pd.DataFrame:
    df = pp_df

    if df is None:
        df = pd.read_csv("past_performance.csv", index_col=0)

    df["FantPos"] = df["FantPos"].astype(str).apply(lambda x: x.strip().upper())

    wr_stat = df[df["FantPos"] == "WR"]["FantPt/Touch"]
    rb_stat = df[df["FantPos"] == "RB"]["FantPt/Touch"]
    te_stat = df[df["FantPos"] == "TE"]["FantPt/Touch"]

    wr_stats = {"mean": wr_stat.mean(), "std": wr_stat.std()}
    rb_stats = {"mean": rb_stat.mean(), "std": rb_stat.std()}
    te_stats = {"mean": te_stat.mean(), "std": te_stat.std()}

    stat_dict = {"WR": wr_stats, "RB": rb_stats, "TE": te_stats}

    df["FantPt/Touch_Z"] = df.apply(_apply_zscore, axis=1, args=([stat_dict]))

    return df
