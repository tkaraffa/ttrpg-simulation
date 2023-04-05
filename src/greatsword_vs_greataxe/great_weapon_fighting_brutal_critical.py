"""
Head-to-head comparison of damage values when both
Great Weapon Fighting and Brutal Critical are used.

Compare 2d6 and 1d12 damage dice with the above feats.

Barbarian characters are assumed to always be raging,
and have their Rage Bonus Damage applied to every
successful hit. They are also assumed to
always use Reckless Attack, which grants
advantage on their attack rolls.
"""

import os

import numpy as np
import plotly.graph_objects as go

from character import Barbarian, Monster
from utils import generate_barbarian_stats
from images_util import get_images_directory


def create_chart(
    names: list,
    results: dict,
    colors: dict,
    title: str,
    filename: str,
    xaxis_title: str = None,
    yaxis_title: str = None,
):
    fig = go.Figure()
    for name in names:
        fig.add_traces(
            [
                go.Bar(
                    x=[level],
                    y=[results[level][name]],
                    marker_color=colors.get(name),
                    texttemplate="%{y}",
                    textposition="inside",
                    textangle=0,
                    showlegend=False,
                    width=[0.4],
                )
                for level in results
            ]
        )
    # dummy data for colors
    for name in colors:
        fig.add_trace(
            go.Bar(
                name=name,
                marker_color=colors.get(name),
                y=[0],
                visible="legendonly",
            )
        )
    fig.update_layout(
        width=600,
        height=300,
        barmode="group",
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        title={
            "text": title,
            "xanchor": "center",
            "yanchor": "top",
            "y": 0.85,
            "x": 0.5,
        },
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )
    fig.update_traces(textfont_size=12)
    fig.write_image(os.path.join(get_images_directory(), filename))


def main():
    REPLICATIONS = 10_000

    colors = {"2d6": "blue", "1d12": "red"}

    for ac in [15, 20, 25]:
        results = dict()
        for level in [5, 10, 15, 20]:
            target_dummy = Monster("Target Dummy", cr=level, ac=ac)
            shared_stats = generate_barbarian_stats(level, gwf=True)
            harrison_sword = Barbarian(
                name="2d6", damage_dice=(6, 2), **shared_stats
            )
            axemillion = Barbarian(
                name="1d12", damage_dice=(12, 1), **shared_stats
            )
            results[f"Level {level}"] = {
                char.name: np.mean(
                    char.attack(
                        target=target_dummy, rolls=REPLICATIONS, advantage=True
                    )
                )
                for char in [harrison_sword, axemillion]
            }
        names = [char.name for char in [harrison_sword, axemillion]]
        create_chart(
            names,
            results,
            colors,
            title=f"Great Weapon Fighting/Brutal Critical AC {ac}",
            filename=f"gwf_bc_ac{ac}.png",
            xaxis_title="Level",
            yaxis_title="Average Damage",
        )


if __name__ == "__main__":
    main()
