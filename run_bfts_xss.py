import numpy as np
from argparse import ArgumentParser

from XSS_bandit import XSS_bandit, XSS_transformations

from bfts.algorithms.bfts import BFTS 
from bfts.algorithms.posteriors.beta import BetaPosterior

import seaborn as sns
import matplotlib.pyplot as plt
import math

plot = False # turn this on if you want to plot the posteriors per arm

parser = ArgumentParser(description="XSS BFTS")

parser.add_argument("-s", "--seed", dest="seed", type=int, required=True)
parser.add_argument("-t", "--time", dest="time", type=int, required=True)
parser.add_argument("-n", "--n_arms", dest="arms", type=int, required=True)
parser.add_argument("-m", "--m", dest="m",type=int, required=True)

args = parser.parse_args()

np.random.seed(args.seed)
bandit = XSS_bandit(args.arms)

posteriors = [BetaPosterior() for x in range(len(bandit.arms))]

algo = BFTS(bandit, args.m, posteriors)

#print header
header = ['m %i' % i for i in range(1, args.m + 1)]
print("t," + ",".join(header), flush=True)

#init posteriors
total_inits = 0
for i in range(len(bandit.arms)):
    for j in range(posteriors[i].times_to_init()):
        reward = bandit.play(i)
        algo.add_reward(i, reward)
        total_inits = total_inits + 1
        #print(str(total_inits) + "," + ",".join(["-1"]*args.m) + "," + str(i) + "," + str(reward), flush=True)

for t in range(1, args.time + 1 - total_inits):
    (J_t, arm, reward) = algo.step(t)
    J_t = [str(i) for i in J_t]
    # print(str(t + total_inits) + "," + ",".join(J_t) + "," + str(arm) + "," + str(reward), flush=True)
    print(str(t + total_inits) + "," + ",".join(J_t), flush=True)

if plot:
    n_techniques = args.arms
    website_1 = 0.25
    website_2 = 0.50
    website_3 = 0.75
    technique_to_mean = {} # first map each technique identifier to its expected mean, this is calculated based on how many filters it is able to bypass

    # the order of the means seems reversed, but that is because we need to find the techniques which have the lowest means
    for technique in range(1, n_techniques+1):
        if technique in range(1, int(n_techniques*website_1)+1):
            technique_to_mean[technique] = 1
        elif technique in range(int(n_techniques*website_1)+1, int(n_techniques*website_2)+1):
            technique_to_mean[technique] = 2/3
        elif technique in range(int(n_techniques*website_2)+1, int(n_techniques*website_3)+1):
            technique_to_mean[technique] = 1/3
        else:
            technique_to_mean[technique] = 0

    techniques = XSS_transformations(n_techniques) # generate the identifiers (in the same order) that are used as arms in the bandit
    identifiers = list(map(lambda x: x("test"), techniques)) # map the techiques on a payload to get identifiers
    real_means = list(map(lambda x: technique_to_mean[x], identifiers)) # retrieve the means from the dictionary

    rewards_per_arm = algo.rewards_per_arm
    n_arms = args.arms
    n_cols = 3
    n_rows = math.ceil(n_arms/3)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))

    axes = axes.flatten() if n_rows > 1 else axes

    for arm_number, rewards in enumerate(rewards_per_arm):
        ax = axes[arm_number]
        ax.hist(rewards, bins=[-0.5, 0.5, 1.5])
        height = real_means[arm_number] * len(rewards)
        ax.plot([0.5, 1.5], [height, height], color='red', linestyle='-')
        ax.set_title(f"Bernoulli of arm {arm_number}")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1/3 * len(rewards), 2/3 * len(rewards), len(rewards)])

    plt.tight_layout(h_pad=4)
    plt.savefig('result_plots/posteriors/bfts/' + f"{n_arms}n_{args.m}m_{args.time}t_bfts_{args.seed}" + '.png', dpi=300)
