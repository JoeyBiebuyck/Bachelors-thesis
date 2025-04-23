import requests
import random
from bfts.bandit import Bandit
import numpy as np
from bfts.environments.gaussian_jun import linear_means

def Bernoulli_bandit(n_arms: int):
    means = linear_means(n_arms)
    #random.Random(1).shuffle(means)
    def reward_fn(mu):
        return lambda: np.random.binomial(1, mu)
    arms = list(map(reward_fn, means))
    return Bandit(arms)