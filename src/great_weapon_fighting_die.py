import functools

import numpy as np

from die import Die


class GWFDie(Die):
    """
    A damage die/dice to use with the feat:
    Great Weapon Fighting
    When you roll a 1 or 2 on a damage die for an Attack
    you make with a melee weapon that you are Wielding with two hands,
    you can Reroll the die and must use the new roll,
    even if the new roll is a 1 or a 2. The weapon must have
    the Two-Handed or Versatile property for you to gain this benefit.
    """

    def __init__(self, sides, number):
        super().__init__(sides=sides, number=number)

    def roll(self, n: int = 1):
        """
        Overloaded function for rolling that allows for
        rerolling 1s and 2s once per attack.

        Construct an array of length n of the sum of x rolls
        e.g., Die(sides=6, number=2).roll(n=10) -> an array of 10 2d6 rolls

        Parameters
        ----------
        n: int
            The number of trials

        Returns
        -------
        roll_arr: np.ndarray
            The array of roll results
        """
        all_arr = []
        for _ in range(self.number):
            roll_arr = np.random.randint(1, self.sides + 1, n)
            roll_arr[roll_arr <= 2] = np.random.randint(
                1, self.sides + 1, len(roll_arr[roll_arr <= 2])
            )
            all_arr.append(roll_arr)
        gwf_roll_arr = functools.reduce(np.add, all_arr)

        return gwf_roll_arr
