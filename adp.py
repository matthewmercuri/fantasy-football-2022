import pandas as pd
import re

FANTASY_PROS_URL = "https://www.fantasypros.com/nfl/adp/overall.php"


def _extract_team_name(x: pd.DataFrame):
    if x["Team Name 1"]:
        return x["Team Name 1"].group(0)
    elif x["Team Name 2"]:
        return x["Team Name 2"].group(0)
    else:
        return ""


def get_fantasy_pros_adp_df() -> pd.DataFrame:
    df = pd.read_html(FANTASY_PROS_URL)[0]

    df = df[["Player Team (Bye)", "AVG"]]

    df["Team Name 1"] = df["Player Team (Bye)"].apply(
        lambda x: re.search("[A-Z]{2}(?<![A-Z]{3})(?![A-Z])", x)
    )
    df["Team Name 2"] = df["Player Team (Bye)"].apply(
        lambda x: re.search("[A-Z]{3}(?<![A-Z]{4})(?![A-Z])", x)
    )
    df["Team"] = df.apply(_extract_team_name, axis=1)

    df["Player Team (Bye)"] = df["Player Team (Bye)"].apply(
        lambda x: re.sub("[A-Z]{2}(?<![A-Z]{3})(?![A-Z])", "", x)
    )
    df["Player Team (Bye)"] = df["Player Team (Bye)"].apply(
        lambda x: re.sub("[A-Z]{3}(?<![A-Z]{4})(?![A-Z])", "", x)
    )

    df["Player Team (Bye)"] = df["Player Team (Bye)"].apply(
        lambda x: re.sub("\(([0-9]*[.]?[0-9]+)\)", "", x)
    )

    df["Player"] = df["Player Team (Bye)"].apply(lambda x: x.strip())

    return df[["Player", "Team", "AVG"]]


adp_df = get_fantasy_pros_adp_df()
adp_df.to_csv("adp_df.csv")
