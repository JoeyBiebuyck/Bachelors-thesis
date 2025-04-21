import numpy as np
from argparse import ArgumentParser
import threading

from XSS_bandit import XSS_bandit
from start_server import start_server

from bfts.algorithms.atlucb import AT_LUCB
from bfts.algorithms.uniform import Uniform
from bfts.run_utils import print_header, run

# n_arms = 20

parser = ArgumentParser(description="XSS ATLUCB")

parser.add_argument("-s", "--seed", dest="seed", type=int, required=True)
parser.add_argument("-t", "--time", dest="time", type=int, required=True)
#parser.add_argument("-a", "--arms", dest="arms", type=int, required=True)
parser.add_argument("-m", "--m", dest="m",type=int, required=True)
parser.add_argument("-e", "--environment", dest="env", type=str, required=False)

args = parser.parse_args()

n_arms = args.arms

np.random.seed(args.seed)
bandit = XSS_bandit(n_arms)
#print(f"bandit has {bandit.arms} arms")

# it is possible to start the servers here, but the terminal output will be filled with the server console outputs
# print("Starting servers:")
# server_thread = threading.Thread(target=start_server, daemon=True)
# server_thread.start()
# print("Servers have been started")

print_header(args.m)
sigma=0.9
alpha=0.99
epsilon=0
algo = AT_LUCB(bandit, args.m, sigma, alpha, epsilon)
#algo = Uniform(bandit, args.m)
run(algo, args.time)