import requests
import random
from bfts.bandit import Bandit
import numpy as np
import sys

def linear_means_no_shuffle(n):
    means = np.linspace(0, 1, n)
    means = list(means)
    random.Random(1).shuffle(means)
    return means

def Bernoulli_bandit(n_arms: int):
    means = linear_means_no_shuffle(n_arms)
    def reward_fn(mu):
        return lambda: np.random.binomial(1, mu)
    arms = list(map(reward_fn, means))
    return Bandit(arms)