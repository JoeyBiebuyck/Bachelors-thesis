import numpy as np
from argparse import ArgumentParser
import threading

from bandits.XSS_bandit import XSS_bandit, XSS_transformations
from start_server import start_server

from bfts.algorithms.uniform import Uniform
from bfts.run_utils import print_header, run
import math
import seaborn as sns
import matplotlib.pyplot as plt
#from global_variables import n_arms

#n_arms = 10 # MUST MANUALLY UPDATE EACH views.py FILE
plot = False # turn this on if you want to plot the posteriors per arm

parser = ArgumentParser(description="XSS ATLUCB")

parser.add_argument("-s", "--seed", dest="seed", type=int, required=True)
parser.add_argument("-t", "--time", dest="time", type=int, required=True)
parser.add_argument("-n", "--n_arms", dest="arms", type=int, required=True)
parser.add_argument("-m", "--m", dest="m",type=int, required=True)
parser.add_argument("-e", "--environment", dest="env", type=str, required=False)

args = parser.parse_args()

#n_arms = args.arms

np.random.seed(args.seed)
bandit = XSS_bandit(args.arms)
#print(f"bandit has {bandit.arms} arms")

# it is possible to start the servers here, but the terminal output will be filled with the server console outputs
# print("Starting servers:")
# server_thread = threading.Thread(target=start_server, daemon=True)
# server_thread.start()
# print("Servers have been started")

print_header(args.m)
algo = Uniform(bandit, args.m)
run(algo, args.time)

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
    n_arms = len(rewards_per_arm)
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
    plt.savefig('result_plots/posteriors/uniform/' + f"{n_arms}n_{args.m}m_{args.time}t_bfts_{args.seed}" + '.png', dpi=300)