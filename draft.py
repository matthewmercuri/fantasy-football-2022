import pandas as pd
from thefuzz import process
from adp import get_fantasy_pros_adp_df
from fantpt_touch import apply_fantpt_touch_stats
from past_performance import get_individuals_df


def _apply_fantpt_touch(x, past_players, pp_df):
    current_player = x["Player"]
    pp_df_player, _ = process.extractOne(current_player, past_players[0])

    return pp_df[pp_df["Player"] == pp_df_player]["FantPt/Touch"].iloc[0]


def _apply_vbd(x, past_players, pp_df):
    current_player = x["Player"]
    pp_df_player, _ = process.extractOne(current_player, past_players[0])

    return pp_df[pp_df["Player"] == pp_df_player]["Fantasy_VBD"].iloc[0]


def assemble_draft_csv() -> pd.DataFrame:
    draft_df = get_fantasy_pros_adp_df()

    pp_df = apply_fantpt_touch_stats(get_individuals_df())
    past_players = pp_df["Player"].tolist()

    draft_df["FantPt/Touch"] = draft_df.apply(
        _apply_fantpt_touch, axis=1, args=([past_players], pp_df)
    )

    draft_df["VBD"] = draft_df.apply(_apply_vbd, axis=1, args=([past_players], pp_df))

    return draft_df


assemble_draft_csv().to_csv("draft.csv")
