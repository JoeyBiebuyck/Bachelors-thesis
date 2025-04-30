import requests
import random
from bfts.bandit import Bandit
import numpy as np
# from environments.gaussian_jun import linear_means

def linear_means_no_shuffle(n): # this is identical to the linear_means function, except for that it does not shuffle the means (for easy verification of correct arm identification)
    # mean_fn = lambda i: .9 * (n - i) / (n - 1)
    # means = list(map(mean_fn, range(n)))
    means = np.linspace(0, 1, n)
    means = list(means)
    random.Random(1).shuffle(means)
    return means

def Bernoulli_bandit(n_arms: int):
    means = linear_means_no_shuffle(n_arms)
    # print(f"these are the means: {means}")
    def reward_fn(mu):
        return lambda: np.random.binomial(1, mu)
    arms = list(map(reward_fn, means))
    return Bandit(arms)