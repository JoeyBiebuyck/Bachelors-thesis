from argparse import ArgumentParser
import csv
import numpy as np
import os
from bandits.Bernoulli_bandit import linear_means_no_shuffle
#from global_variables import n_arms

parser = ArgumentParser(description="postprocess")

parser.add_argument("-c", "--csv_fn", dest="csv_fn", type=str, required=True)
parser.add_argument("-n", "--n_arms", dest="arms", type=int, required=True)
parser.add_argument("-s", "--statistic", dest="stat", type=str, required=True)
parser.add_argument("-m", "--m", dest="m", type=int, required=True)

args = parser.parse_args()

means = linear_means_no_shuffle(args.arms)

real_means = np.array(means)
real_m_top = np.argsort(-real_means)[:args.m]

#print the output header
if args.stat == "prop_and_sum":
    print("t," + "prop," + "sum", flush=True)
else:
    print("t," + args.stat, flush=True)

with open(args.csv_fn) as csv_file:
    read_csv = csv.reader(csv_file, delimiter=',')
    header = next(read_csv)
    #first column is the time, the rest are the top arms
    for row in read_csv:
        time = int(row[0])
        m_top = list(map(int, row[1:1+args.m]))

        if args.stat == "min":
            min_ = np.min(real_means[m_top])
            print(str(time) + "," + str(min_))
        elif args.stat == "sum":
            sum_ = np.sum(real_means[m_top])
            print(str(time) + "," + str(sum_))
        elif args.stat == "prop_of_success":
            i = set(real_m_top).intersection(set(m_top))
            prop = len(i) / args.m
            print(str(time) + "," + str(prop))
        elif args.stat == "prop_and_sum": # new statistic for both proportion of success and sum of m-top means
            i = set(real_m_top).intersection(set(m_top))
            prop = len(i) / args.m
            sum_ = np.sum(real_means[m_top])
            print(str(time) + "," + str(prop) + "," + str(sum_))
        else:
            raise ValueError("Invalid statistic, choose from:" + \
                    "[min, sum, prop_of_success, prop_and_sum]")
