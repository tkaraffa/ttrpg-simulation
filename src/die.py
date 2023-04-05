import numpy as np


class Die:
    """
    A class that supports generating arrays of discrete random numbers
    """

    def __init__(self, sides: int, number: int = 1) -> None:
        self.sides = sides
        self.number = number  # by default, only roll 1 die
        self.expected_value = ((1 + self.sides) / 2) * (self.number)

    def display(self):
        return f"{self.number}d{self.sides}"

    def roll(self, n: int = 1):
        """
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
        roll_arr = np.sum(
            np.random.randint(1, self.sides + 1, (n, self.number)), axis=1
        )

        return roll_arr

    def sum_roll(self, n: int = 1):
        """
        Calculate the sum of n rolls
        Use when calculating damage for misses, hits, and criticals

        Parameters
        ----------
        n: int
            The number of rolls to sum

        Returns
        -------
        roll_sum: int
            The sum of all rolls
        """
        roll_sum = np.sum(self.roll(n))
        return roll_sum

    def avg_roll(self, n=1):
        """
        Calculate the average of n rolls

        Parameters
        ----------
        n: int
            The number of rolls to average
        x: int
            The number of dice to roll for each trial

        Returns
        -------
        roll_avg: float
            The average of all rolls
        """
        roll_avg = np.mean(self.roll(n))
        return roll_avg


class D20(Die):
    """
    A single D20 used for rolling attacks
    """

    def __init__(self):
        super().__init__(sides=20, number=1)

    def roll_with_advantage(self, n=1):
        """
        Roll a D20 n*2 times, keeping the better of each pair of rolls
        """
        return np.maximum(self.roll(n), self.roll(n))

    def roll_with_disadvantage(self, n=1):
        """
        Roll a D20 n*2 times, keeping the worse of each pair of rolls
        """
        return np.minimum(self.roll(n), self.roll(n))
