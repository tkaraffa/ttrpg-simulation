"""
This simulation seeks to address the question: should you use a shield?
Generally, the tradeoff is relevant when considering whether to use
a shield OR to two-hand a weapon, which increases the damage it deals.

In this simulation, we will investigate the case of a Fighter class
using a longsword. When one-handed, it uses 1d8 for its damage die,
when two-handed, 1d10. The tradeoff is that when one-handing,
the other hand is free to use a shield, which offers a +2 bonus
to Armor Class, and makes the character more difficult to hit.

All other parameters will be held equal for the duelling characters -
level is scaled equally, with hit bonus, damage bonus, base AC, and other
stat modifiers increasing linearly with level. The hit die is set as 1d10,
which is native to the Fighter class.
Statistics may vary slightly, due to random variable generation; e.g.,
even though the characters both use the same hit die, each level
involves rolling the hit die and adding its value to the characters
total Hit Points, so if one character consistently rolls well and
the other does not, their Hit Points will differ significantly.

Each replication will have its own random variables - the rolls on Hit
Points at each level up, the to-hit rolls, and the damage rolls.
These will be averaged across all replications to provide a sample mean of
wins/losses that approaches the true mean of wins/losses by
the Central Limit Theorem.

Each set of parameters (level, hit die, and AC) will be considered its own
simulation, with the outputs averaged within that simulation only. However,
in the overarching analysis, all simulations will be considered cohesively.
"""
import os
import math

import numpy as np
from plotly import graph_objects as go

from character import Character, Monster
from utils import fight, generate_fighter_stats
from images_util import get_images_directory


def create_chart(
    results: dict,
    colors: dict,
    title: str,
    filename: str,
    replications: int,
):
    """
    Create a bar chart to track simulation results

    Parameters
    ---------
    results: dict
        Dictionary of results from simulation
    colors: dict
        Dictionary of colors for names of characters
    title: str
        Title for the chart
    filename: str
        Name of the file for the chart
    replications: int
        Number of replications used in the simulation
    """

    chart_data = []
    for level in results:
        chart_data.extend(
            go.Bar(
                x=[str(level)],
                y=[result],
                name=name,
                marker_color=colors.get(name),
                texttemplate="%{y}",
                textposition="inside",
                textangle=0,
                showlegend=False,
            )
            for name, result in zip(results[level][0], results[level][1])
        )

    fig = go.Figure(data=chart_data)
    # add in dummy data for legend
    for name in colors:
        fig.add_trace(
            go.Bar(
                name=name,
                marker_color=colors.get(name),
                y=[0],
                visible="legendonly",
            )
        )
    fig.add_hline(y=replications / 2)
    fig.update_layout(
        width=800,
        height=400,
        barmode="stack",
        xaxis_title="Level",
        yaxis_title="Replications",
        title={
            "text": title,
            "xanchor": "center",
            "yanchor": "top",
            "y": 0.85,
            "x": 0.5,
        },
    )
    fig.write_image(os.path.join(get_images_directory(), filename))


def main():
    REPLICATIONS = 10_000
    levels = range(1, 21)
    char_fight_results = dict()
    longsword_mon_fight_results = dict()
    shield_mon_fight_results = dict()

    for level in levels:
        # assume both players have equal AC, which increases
        # by 1 every 4 levels
        # up to a non-shield value of 22 at level 20
        ac = 17 + math.floor(level / 4)
        shared_stats = generate_fighter_stats(level)
        longswordington = Character(
            name="Longswordington",
            **shared_stats,
            ac=ac,
            damage_dice=(10, 1),
        )
        shieldsworth = Character(
            name="Shieldsworth",
            **shared_stats,
            ac=ac + 2,
            damage_dice=(8, 1),
        )
        monster = Monster(
            name="Zombie",
            cr=level,
        )

        char_fight_results[level] = np.unique(
            [
                fight(
                    longswordington,
                    shieldsworth,
                )
                for _ in range(REPLICATIONS)
            ],
            return_counts=True,
        )
        longsword_mon_fight_results[level] = np.unique(
            [
                fight(
                    longswordington,
                    monster,
                )
                for _ in range(REPLICATIONS)
            ],
            return_counts=True,
        )
        shield_mon_fight_results[level] = np.unique(
            [
                fight(
                    shieldsworth,
                    monster,
                )
                for _ in range(REPLICATIONS)
            ],
            return_counts=True,
        )

    # generate combinations of results for each chart
    tie = {"Tie": "green"}
    ls = {"Longswordington": "blue"}
    sh = {"Shieldsworth": "red"}
    mon = {"Zombie": "purple"}
    char_fight_colors = {**tie, **ls, **sh}
    longsword_mon_fight_colors = {**tie, **ls, **mon}
    shield_mon_fight_colors = {**tie, **sh, **mon}

    create_chart(
        char_fight_results,
        char_fight_colors,
        "Longswordington vs Shieldsworth",
        "shield_battle.png",
        REPLICATIONS,
    )
    create_chart(
        longsword_mon_fight_results,
        longsword_mon_fight_colors,
        "Longswordington vs Monster",
        "ls_mon.png",
        REPLICATIONS,
    )
    create_chart(
        shield_mon_fight_results,
        shield_mon_fight_colors,
        "Shieldsworth vs Monster",
        "sh_mon.png",
        REPLICATIONS,
    )


if __name__ == "__main__":
    main()
