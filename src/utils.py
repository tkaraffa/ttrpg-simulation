import os
from pathlib import Path

import numpy as np

from character import Character


def _generate_character_stats(
    level: int,
    level_options: list,
    level_apis: list,
    hit_die: int = None,
) -> dict:
    """
    Prototype function for generating character stats.
    """
    modifiers = np.select(level_options, level_apis)

    # assume the character starts with a +3 strength modifier
    # and a +2 constitution modifier, i.e., a 16 strength and 14 constitution
    # these are standard choices for a strength-based charcter
    str_modifier = 3 + modifiers[0]
    con_modifier = 2 + modifiers[1]
    stats = dict(
        level=level,
        strength_modifier=str_modifier,
        constitution_modifier=con_modifier,
    )
    if hit_die is not None:
        stats = {
            **stats,
            "hit_die": (hit_die, 1),
        }
    return stats


def generate_fighter_stats(level: int) -> dict:
    """
    Generate dict of random variables to use as statistics
    for a Fighter class character.

    Parameters
    ----------
    level: int
        The level of the character, which corresponds
        to their relative strength

    Returns
    -------
    stats: dict
        Appropriately-named dict of stats
        to pass into a Character object
    """
    levels = [
        1 <= level < 4,
        4 <= level < 6,
        6 <= level < 8,
        8 <= level < 12,
        12 <= level < 14,
        14 <= level,
    ]
    apis = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (2, 3)]
    # by the time you get to level 14, if you've exclusively been
    # putting apis into str or con, they will both be 20,
    # and so we don't need to track the two beyond 14th level

    # technically you get 2 points,
    # but it rarely makes sense to use them for anything
    # besides increasing your modifier by 1,
    # so we'll just call it a +1

    # assume the character progresses alternatingly, i.e.,
    # at level 4, adds +1 to str modifier, at level 6, adds
    # +1 to con modifier, alternating until level 12,
    # then finishing off con to +5 at level 14

    stats = _generate_character_stats(level, levels, apis, hit_die=10)
    return stats


def generate_barbarian_stats(level: int, gwf: bool = False) -> dict:
    """
    Generate dict of random variables to use as statistics
    for a Barbarian class character.

    Parameters
    ----------
    level: int
        The level of the character, which corresponds
        to their relative strength
    gwf: bool
        Whether the Great Weapon Fighting feat is taken
        at 4th level (instead of an ability point increase).

    Returns
    -------
    stats: dict
        Appropriately-named dict of stats
        to pass into a Character object
    """
    levels = [
        1 <= level < 4,
        4 <= level < 8,
        8 <= level < 12,
        12 <= level < 16,
        16 <= level,
    ]
    if gwf is True:
        apis = [(0, 0), (0, 0), (1, 0), (1, 1), (2, 1)]
    else:
        apis = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]

    stats = _generate_character_stats(level, levels, apis)
    return {**stats, "great_weapon_fighting": gwf}


def find_defeat_index(target: Character, damage_arr: np.ndarray) -> int:
    """
    Find the index at which the cumulative damage from an array
    of damage rolls exceeds the hp of the target

    Parameters
    ----------
    target: Character
        The target whose hp to use to calculate defeat
    damage_arr: np.ndarray
        The array of damage rolls

    Returns
    -------
    defeat_index: int
        The index of the damage array
    """
    total_damage_arr = np.cumsum(damage_arr)
    if total_damage_arr[-1] < target.hp:
        return len(damage_arr)
    defeat_index = (total_damage_arr >= target.hp).argmax()
    return defeat_index


def fight(char1: Character, char2: Character, rolls: int = 500) -> str:
    """
    Simulate a single one-on-one fight between two Characters.

    Parameters
    ----------
    char1: Character
    char2: Character
    rolls: int = 500
        The number of rounds for a single fight
        Should be long enough to ensure one character wins

    Returns
    -------
    winner: str
        The name of the winner
        If neither Character was reduced to 0 hit points in the
        provided number of rounds, returns "Tie"
    """
    char1_damage_arr = char1.attack(char2, rolls)
    char2_damage_arr = char2.attack(char1, rolls)

    char1_defeated_at = find_defeat_index(char1, char2_damage_arr)
    char2_defeated_at = find_defeat_index(char2, char1_damage_arr)
    if rolls == char1_defeated_at == char2_defeated_at:
        winner = "Tie"
    while char1.initiative == char2.initiative:
        char1.roll_initiative()
        char2.roll_initiative()

    if (char1_defeated_at > char2_defeated_at) or (
        char1.initiative > char2.initiative
        and char1_defeated_at == char2_defeated_at
    ):
        winner = char1.name
    elif (char2_defeated_at > char1_defeated_at) or (
        char2.initiative > char1.initiative
        and char2_defeated_at == char1_defeated_at
    ):
        winner = char2.name
    return winner
