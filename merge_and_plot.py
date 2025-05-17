import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser


parser = ArgumentParser(description="XSS merge and plot")

parser.add_argument("-d", "--dir", dest="dir", type=str, required=True) # directory it will find the files in
parser.add_argument("-t", "--time", dest="time", type=int, required=True)
parser.add_argument("-n", "--n_arms", dest="arms", type=int, required=True)
parser.add_argument("-m", "--m", dest="m",type=int, required=True)
parser.add_argument("-s", "--stat", dest="stat", type=str, required=True)

args = parser.parse_args()

dir = args.dir
stat = args.stat

# merge the experiments

if stat == "prop_and_sum": # this statistic has an extra column, so must be merged differently
    merged_bfts_df = pd.read_csv(dir + "/bfts-1." + stat)
    merged_bfts_df.rename(columns={"prop": "prop_1", "sum": "sum_1"})

    for i in range(2, 101):
        old_df = merged_bfts_df
        new_filename = dir + "/bfts-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_bfts_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

    merged_atlucb_df = pd.read_csv(dir + "/atlucb-1." + stat)
    merged_atlucb_df.rename(columns={"prop": "prop_1", "sum": "sum_1"})

    for i in range(2, 101):
        old_df = merged_atlucb_df
        new_filename = dir + "/atlucb-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_atlucb_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

    merged_uniform_df = pd.read_csv(dir + "/uniform-1." + stat)
    merged_uniform_df.rename(columns={"prop": "prop_1", "sum": "sum_1"})

    for i in range(2, 101):
        old_df = merged_uniform_df
        new_filename = dir + "/uniform-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_uniform_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))
else:
    merged_bfts_df = pd.read_csv(dir + "/bfts-1." + stat)
    merged_bfts_df.rename(columns={stat: stat + "_1"})

    for i in range(2, 101):
        old_df = merged_bfts_df
        new_filename = dir + "/bfts-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_bfts_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

    merged_atlucb_df = pd.read_csv(dir + "/atlucb-1." + stat)
    merged_atlucb_df.rename(columns={stat: stat + "_1"})

    for i in range(2, 101):
        old_df = merged_atlucb_df
        new_filename = dir + "/atlucb-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_atlucb_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

    merged_uniform_df = pd.read_csv(dir + "/uniform-1." + stat)
    merged_uniform_df.rename(columns={stat: stat + "_1"})

    for i in range(2, 101):
        old_df = merged_uniform_df
        new_filename = dir + "/uniform-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_uniform_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

merged_bfts_df.to_csv(dir + "/results/merged_bfts_" + stat + ".csv", index=False)
merged_atlucb_df.to_csv(dir + "/results/merged_atlucb_" + stat + ".csv", index=False)
merged_uniform_df.to_csv(dir + "/results/merged_uniform_" + stat + ".csv", index=False)

# plot the experiments

plt.style.use('default')
sns.set_style("whitegrid", {'axes.grid': False})

plt.figure(figsize=(10, 7))

def make_csv_plotable(file_path, method_name):
    df = pd.read_csv(file_path)
    # extract timesteps from csv
    timesteps = df.iloc[:, 0].values
    # extract statistic values from csv
    y_values = df.iloc[:, 1:].values
    # calculate the mean value for every timestep
    mean_values = np.mean(y_values, axis=1)
    # calculate standard deviation (for confidence intervals) for every timestep
    std_values = np.std(y_values, axis=1)

    plotable_df = pd.DataFrame({
        'samples': timesteps,
        'method': method_name,
        'value': mean_values,
        'lower': np.maximum(0, mean_values - std_values),  # to make sure there are no negative values
        'upper': np.minimum(1, mean_values + std_values)   # to make sure there are no values greater than 1
    })

    return plotable_df

results_dir = dir + "/results"

uniform_df = make_csv_plotable(results_dir + "/merged_uniform_" + stat + ".csv", "Uniform")
atlucb_df = make_csv_plotable(results_dir + "/merged_atlucb_" + stat + ".csv", "AT-LUCB")
bfts_df = make_csv_plotable(results_dir + "/merged_bfts_" + stat + ".csv", "BFTS")

combined_df = pd.concat([uniform_df, atlucb_df, bfts_df], ignore_index=True)

for method, color in zip(["Uniform", "AT-LUCB", "BFTS"], ["blue", "green", "red"]):
    method_data = combined_df[combined_df['method'] == method]

    plt.fill_between(
        method_data['samples'], 
        method_data['lower'], 
        method_data['upper'],
        color=color, 
        alpha=0.3
    )

    sns.lineplot(
        x='samples', 
        y='value',
        data=method_data,
        color=color,
        linewidth=2,
        label=method
    )

# Set the axis labels with LaTeX formatting
plt.xlabel(r'$\#$ of samples', fontsize=14) # $\times 10^4$
plt.ylabel(r'$|J(t) \cap J^*|/m$', fontsize=14)

# Configure the legend
plt.legend(fontsize=12, frameon=True, facecolor='white', edgecolor='lightgray')

# Set y-axis limits to match the example
plt.ylim(0, 1)

# Remove the top and right spines for a cleaner look
sns.despine()

# Add a tight layout
plt.tight_layout(pad=1.5, rect=[0, 0, 1, 0.95])
parent_dir, experiment_name = dir.split('/')
arms, timesteps, top_m, extra = experiment_name.split('_', 3)

n = args.arms
m = args.m
t = args.time

plt.title(f"n={n}, m={m}, t={t}")

plt.savefig(results_dir + '/' + experiment_name + '.png', dpi=300)

# save ook op een plek die in git zit
plt.savefig('result_plots/' + experiment_name + '.png', dpi=300)

# Show the plot
plt.show()