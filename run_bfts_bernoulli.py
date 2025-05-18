import numpy as np
from argparse import ArgumentParser

from bandits.Bernoulli_bandit import Bernoulli_bandit
from bfts.algorithms.bfts import BFTS 
from bfts.algorithms.posteriors.beta import BetaPosterior

parser = ArgumentParser(description="BFTS Bernoulli")

parser.add_argument("-s", "--seed", dest="seed", type=int, required=True)
parser.add_argument("-t", "--time", dest="time", type=int, required=True)
parser.add_argument("-n", "--n_arms", dest="arms", type=int, required=True)
parser.add_argument("-m", "--m", dest="m",type=int, required=True)

args = parser.parse_args()

np.random.seed(args.seed)

bandit = Bernoulli_bandit(args.arms)
posteriors = [BetaPosterior() for x in range(len(bandit.arms))]

algo = BFTS(bandit, args.m, posteriors)

#print header
header = ['m %i' % i for i in range(1, args.m + 1)]
print("t," + ",".join(header) + ",arm,reward", flush=True)

#init posteriors
total_inits = 0
for i in range(len(bandit.arms)):
    for j in range(posteriors[i].times_to_init()):
        reward = bandit.play(i)
        algo.add_reward(i, reward)
        total_inits = total_inits + 1
        print(str(total_inits) + "," + ",".join(["-1"]*args.m) + "," + str(i) + "," + str(reward), flush=True)

for t in range(1, args.time + 1 - total_inits):
    (J_t, arm, reward) = algo.step(t)
    J_t = [str(i) for i in J_t]
    # print(str(t + total_inits) + "," + ",".join(J_t) + "," + str(arm) + "," + str(reward), flush=True)
    print(str(t + total_inits) + "," + ",".join(J_t), flush=True)