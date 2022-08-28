import pandas as pd
from thefuzz import process
import math
from adp import get_fantasy_pros_adp_df
from fantpt_touch import apply_fantpt_touch_stats
from past_performance import get_individuals_df

PARTICIPANTS = 12


def _apply_fantpt_touch(x, past_players, pp_df):
    current_player = x["Player"]
    pp_df_player, _ = process.extractOne(current_player, past_players[0])

    return pp_df[pp_df["Player"] == pp_df_player]["FantPt/Touch"].iloc[0]


def _apply_fantpt_touch_zscore(x, past_players, pp_df):
    current_player = x["Player"]
    pp_df_player, _ = process.extractOne(current_player, past_players[0])

    return pp_df[pp_df["Player"] == pp_df_player]["FantPt/Touch_Z"].iloc[0]


def _apply_vbd(x, past_players, pp_df):
    current_player = x["Player"]
    pp_df_player, _ = process.extractOne(current_player, past_players[0])

    return pp_df[pp_df["Player"] == pp_df_player]["Fantasy_VBD"].iloc[0]


def _apply_draft_pick(x, participants):
    rank = x["Index"]

    pick_in_round = math.ceil(rank / participants) if rank > participants else 1
    pick_number = rank % participants

    if pick_number == 0:
        pick_number = participants

    return f"Round {pick_in_round}, Pick {pick_number}"


def _final_cleanup(df: pd.DataFrame = None) -> pd.DataFrame:
    final_columns = ["Player", "Team", "AVG", "POS", "FantPt/Touch_Z", "VBD", "Pick"]

    if df is None:
        df = pd.read_csv("draft.csv", index_col=0)

    df = df[final_columns].convert_dtypes()
    df["FantPt/Touch_Z"] = df["FantPt/Touch_Z"].round(3)

    return df


def assemble_draft_csv(participants: int = PARTICIPANTS) -> pd.DataFrame:
    draft_df = get_fantasy_pros_adp_df()

    pp_df = apply_fantpt_touch_stats(get_individuals_df())
    past_players = pp_df["Player"].tolist()

    draft_df["FantPt/Touch"] = draft_df.apply(
        _apply_fantpt_touch, axis=1, args=([past_players], pp_df)
    )

    draft_df["FantPt/Touch_Z"] = draft_df.apply(
        _apply_fantpt_touch_zscore, axis=1, args=([past_players], pp_df)
    )

    draft_df["VBD"] = draft_df.apply(_apply_vbd, axis=1, args=([past_players], pp_df))

    draft_df.sort_values(by="AVG", ascending=True, inplace=True)
    draft_df.reset_index(inplace=True)
    draft_df["Index"] = draft_df.index + 1
    draft_df["Pick"] = draft_df.apply(_apply_draft_pick, axis=1, args=([participants]))

    draft_df = _final_cleanup(draft_df)

    return draft_df


assemble_draft_csv().to_csv("draft.csv")
