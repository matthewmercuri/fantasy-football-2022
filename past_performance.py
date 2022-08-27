import pandas as pd

INDIVIDUALS_URL = "https://www.pro-football-reference.com/years/2021/fantasy.htm"

MIN_GAMES = 8


def get_individuals_df() -> pd.DataFrame:
    df = pd.read_html(INDIVIDUALS_URL)[0]

    df.columns = df.columns.droplevel(0)

    df = df[df["G"] != "G"]

    df = df[df["G"] >= MIN_GAMES]

    df["Player"] = df["Player"].apply(lambda x: x.replace("+", ""))
    df["Player"] = df["Player"].apply(lambda x: x.replace("*", ""))
    print(df)


get_individuals_df()
