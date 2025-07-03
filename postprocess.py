from argparse import ArgumentParser
import csv
import numpy as np
from bandits.XSS_bandit import XSS_transformations, XSS_bandit
import os

parser = ArgumentParser(description="postprocess")

parser.add_argument("-c", "--csv_fn", dest="csv_fn", type=str, required=True)
parser.add_argument("-n", "--n_arms", dest="arms", type=int, required=True)
parser.add_argument("-s", "--statistic", dest="stat", type=str, required=True)
parser.add_argument("-m", "--m", dest="m", type=int, required=True)

args = parser.parse_args()

n_techniques = args.arms
n_websites = 9
# match these values with those in the views.py files
website_1 = 0.1
website_2 = 0.2
website_3 = 0.3
website_4 = 0.4
website_5 = 0.5
website_6 = 0.6
website_7 = 0.7
website_8 = 0.8
website_9 = 0.9
technique_to_mean = {} # first map each technique identifier to its expected mean, this is calculated based on how many filters it is able to bypass

# calculate the mean of each technique (this is based on how many websites it can evade the filter of)
# if the technique is in the range, that means all websites of that number and higher block its evasion attempts
for technique in range(1, n_techniques+1):
    if technique in range(1, int(n_techniques*website_1)+1):
        technique_to_mean[technique] = 0
    elif technique in range(int(n_techniques*website_1)+1, int(n_techniques*website_2)+1):
        technique_to_mean[technique] = 1/n_websites
    elif technique in range(int(n_techniques*website_2)+1, int(n_techniques*website_3)+1):
        technique_to_mean[technique] = 2/n_websites
    elif technique in range(int(n_techniques*website_3)+1, int(n_techniques*website_4)+1):
        technique_to_mean[technique] = 3/n_websites
    elif technique in range(int(n_techniques*website_4)+1, int(n_techniques*website_5)+1):
        technique_to_mean[technique] = 4/n_websites
    elif technique in range(int(n_techniques*website_5)+1, int(n_techniques*website_6)+1):
        technique_to_mean[technique] = 5/n_websites
    elif technique in range(int(n_techniques*website_6)+1, int(n_techniques*website_7)+1):
        technique_to_mean[technique] = 6//n_websites
    elif technique in range(int(n_techniques*website_7)+1, int(n_techniques*website_8)+1):
        technique_to_mean[technique] = 7/n_websites
    elif technique in range(int(n_techniques*website_8)+1, int(n_techniques*website_9)+1):
        technique_to_mean[technique] = 8/n_websites
    else:
        technique_to_mean[technique] = 1

bandit = XSS_bandit(n_techniques)
techniques = XSS_transformations(n_techniques) # generate the identifiers (in the same order) that are used as arms in the bandit
identifiers = list(map(lambda x: x("test"), techniques)) # map the techiques on a payload to get identifiers
real_means = list(map(lambda x: technique_to_mean[x], identifiers)) # retrieve the means from the dictionary

real_means = np.array(real_means)
real_m_top = np.argsort(-real_means)[:args.m] # the indexes of the m-top arms

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
