"""
Compare 2d6 and 1d12 damage dice with and without the
Great Weapon Fighting feat, which allows 1s and 2s to be
rerolled once.
"""

import os
from collections import OrderedDict

import plotly.graph_objects as go

from die import Die
from great_weapon_fighting_die import GWFDie
from images_util import get_images_directory


def create_chart(
    data: dict, filename: str, xaxis_title: str = None, yaxis_title: str = None
):
    fig = go.Figure(
        go.Bar(
            x=list(data.keys()),
            y=list(data.values()),
            texttemplate="%{y}",
            textposition="inside",
        )
    )
    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        width=800,
        height=400,
    )
    fig.write_image(os.path.join(get_images_directory(), filename))


def main():
    replications = 10_000
    greatsword_die = (6, 2)
    greataxe_die = (12, 1)
    filename = "sword_axe.png"
    # set up each die type with corresponding name
    params = list(zip(["Vanilla", "Great Weapon Fighting"], [Die, GWFDie]))

    greatsword = {
        f"{name}\n{die_type(*greatsword_die).display()}": die_type(
            *greatsword_die
        ).avg_roll(replications)
        for name, die_type in params
    }
    greataxe = {
        f"{name} - {die_type(*greataxe_die).display()}": die_type(
            *greataxe_die
        ).avg_roll(replications)
        for name, die_type in params
    }
    data = OrderedDict(**greatsword, **greataxe)

    create_chart(
        data,
        filename,
        xaxis_title="Weapon",
        yaxis_title="Average Damage",
    )


if __name__ == "__main__":
    main()
