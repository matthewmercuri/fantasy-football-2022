import pandas as pd

INDIVIDUALS_URL = "https://www.pro-football-reference.com/years/2021/fantasy.htm"

MIN_GAMES = 8
MIN_TOUCHES = 20
TOUCH_COLUMNS = ["Rushing_Att", "Receiving_Rec"]


def get_individuals_df() -> pd.DataFrame:
    df = pd.read_html(INDIVIDUALS_URL)[0]

    header_cols = df.columns

    df.columns = [
        f"{first_level}_{second_level}" if first_level[0:3] != "Unn" else second_level
        for first_level, second_level in header_cols
    ]

    df = df[df["Games_G"] != "G"]

    df["Games_G"] = df["Games_G"].astype(int)

    df = df[df["Games_G"] >= MIN_GAMES]

    df["Player"] = df["Player"].apply(lambda x: x.replace("+", ""))
    df["Player"] = df["Player"].apply(lambda x: x.replace("*", ""))

    df["Touches"] = df[TOUCH_COLUMNS].astype(float).sum(axis="columns")
    df["FantPt/Touch"] = df["Fantasy_FantPt"].astype(float) / df["Touches"]
    df["FantPt/Touch"] = df.apply(
        lambda x: 0
        if x["Touches"] < MIN_TOUCHES or x["FantPos"] in ["QB", "K"]
        else x["FantPt/Touch"],
        axis=1,
    )

    return df


get_individuals_df().to_csv("past_performance.csv")
