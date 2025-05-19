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
n = args.arms
m = args.m
t = args.time

# merge the experiments
if stat == "prop_and_sum": # this statistic has an extra column, so must be merged differently
    merged_bfts_df = pd.read_csv(dir + "/bfts-1." + stat)
    merged_bfts_df = merged_bfts_df.rename(columns={"prop": "prop_1", "sum": "sum_1"})

    for i in range(2, 101):
        old_df = merged_bfts_df
        new_filename = dir + "/bfts-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_bfts_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

    merged_atlucb_df = pd.read_csv(dir + "/atlucb-1." + stat)
    merged_atlucb_df = merged_atlucb_df.rename(columns={"prop": "prop_1", "sum": "sum_1"})

    for i in range(2, 101):
        old_df = merged_atlucb_df
        new_filename = dir + "/atlucb-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_atlucb_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

    merged_uniform_df = pd.read_csv(dir + "/uniform-1." + stat)
    merged_uniform_df = merged_uniform_df.rename(columns={"prop": "prop_1", "sum": "sum_1"})

    for i in range(2, 101):
        old_df = merged_uniform_df
        new_filename = dir + "/uniform-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_uniform_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

    merged_bfts_df.to_csv(dir + "/results/merged_bfts_" + stat + ".csv", index=False)
    merged_atlucb_df.to_csv(dir + "/results/merged_atlucb_" + stat + ".csv", index=False)
    merged_uniform_df.to_csv(dir + "/results/merged_uniform_" + stat + ".csv", index=False)
else:
    merged_bfts_df = pd.read_csv(dir + "/bfts-1." + stat)
    merged_bfts_df = merged_bfts_df.rename(columns={stat: stat + "_1"})

    for i in range(2, 101):
        old_df = merged_bfts_df
        new_filename = dir + "/bfts-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_bfts_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

    merged_atlucb_df = pd.read_csv(dir + "/atlucb-1." + stat)
    merged_atlucb_df = merged_atlucb_df.rename(columns={stat: stat + "_1"})

    for i in range(2, 101):
        old_df = merged_atlucb_df
        new_filename = dir + "/atlucb-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_atlucb_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

    merged_uniform_df = pd.read_csv(dir + "/uniform-1." + stat)
    merged_uniform_df = merged_uniform_df.rename(columns={stat: stat + "_1"})

    for i in range(2, 101):
        old_df = merged_uniform_df
        new_filename = dir + "/uniform-" + str(i) + "." + stat
        new_df = pd.read_csv(new_filename)
        merged_uniform_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))
    
    merged_bfts_df.to_csv(dir + "/results/merged_bfts_" + stat + ".csv", index=False)
    merged_atlucb_df.to_csv(dir + "/results/merged_atlucb_" + stat + ".csv", index=False)
    merged_uniform_df.to_csv(dir + "/results/merged_uniform_" + stat + ".csv", index=False)

def make_csv_plotable(file_path, method_name):

    if stat == "prop_and_sum": # for this statistic there are 2 statistics in the files, so they must be extracted differently
        df = pd.read_csv(file_path)
        # extract timesteps from csv
        timesteps = df.iloc[:, 0].values
        # extract statistic values from csv
        y_values = df.iloc[:, range(1, df.shape[1], 2)].values # the columns are alternating, so only every other column is the same statistic
        # calculate the mean value for every timestep
        mean_values = np.mean(y_values, axis=1) # idem
        # calculate standard deviation (for confidence intervals) for every timestep
        std_values = np.std(y_values, axis=1)
        sum_y_values = df.iloc[:, range(2, df.shape[1], 2)].values
        sum_mean_values = np.mean(sum_y_values, axis=1)
        sum_std_values = np.std(sum_y_values, axis=1)
        df_dict = {
            'samples': timesteps,
            'method': method_name,
            'value': mean_values,
            'lower': np.maximum(0, mean_values - std_values),  # to make sure there are no negative values
            'upper': np.minimum(1, mean_values + std_values),   # to make sure there are no values greater than 1
            'sum_mu': sum_mean_values,
            'sum_mu_lower': np.maximum(0, sum_mean_values - sum_std_values),
            'sum_mu_upper': np.minimum(m, sum_mean_values + sum_std_values),
        }
    else: # if there is only 1 statistic in the files
        df = pd.read_csv(file_path)
        # extract timesteps from csv
        timesteps = df.iloc[:, 0].values
        # extract statistic values from csv
        y_values = df.iloc[:, 1:].values
        # calculate the mean value for every timestep
        mean_values = np.mean(y_values, axis=1)
        # calculate standard deviation (for confidence intervals) for every timestep
        std_values = np.std(y_values, axis=1)

        df_dict = {
            'samples': timesteps,
            'method': method_name,
            'value': mean_values,
            'lower': np.maximum(0, mean_values - std_values),  # to make sure there are no negative values
            'upper': np.minimum(1, mean_values + std_values),   # to make sure there are no values greater than 1
        }


    plotable_df = pd.DataFrame(df_dict)

    return plotable_df

results_dir = dir + "/results"

uniform_df = make_csv_plotable(results_dir + "/merged_uniform_" + stat + ".csv", "Uniform")
atlucb_df = make_csv_plotable(results_dir + "/merged_atlucb_" + stat + ".csv", "AT-LUCB")
bfts_df = make_csv_plotable(results_dir + "/merged_bfts_" + stat + ".csv", "BFTS")

combined_df = pd.concat([uniform_df, atlucb_df, bfts_df], ignore_index=True)
combined_df.to_csv(dir + "/results/merged_DF.csv", index=False)

parent_dir, experiment_name = dir.split('/')
arms, timesteps, top_m, extra = experiment_name.split('_', 3)

# plot the experiments
plt.style.use('default')
sns.set_style("whitegrid", {'axes.grid': False})

# make 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# plot the first plot (left), this is the proportion of correctly identified arms (this plot could be any statistic, the labels would just be wrong then)
for method, color in zip(["Uniform", "AT-LUCB", "BFTS"], ["blue", "green", "red"]):
    method_data = combined_df[combined_df['method'] == method]
    
    # adjust for AT-LUCB taking 2 samples per time step
    if method == "AT-LUCB":
        method_data = method_data.assign(actual_samples=method_data['samples'] * 2)
    else:
        method_data = method_data.assign(actual_samples=method_data['samples'])

    ax1.fill_between(
        method_data['actual_samples'], 
        method_data['lower'], 
        method_data['upper'],
        color=color, 
        alpha=0.3
    )
    
    sns.lineplot(
        x='actual_samples', 
        y='value',
        data=method_data,
        color=color,
        linewidth=2,
        label=method,
        ax=ax1
    )

# set the labels
ax1.set_xlabel(r'$\#$ of samples', fontsize=14)
ax1.set_ylabel(r'$|J(t) \cap J^*|/m$', fontsize=14)
ax1.set_ylim(0, 1)
ax1.set_xlim(0, t)
ax1.legend(fontsize=12, frameon=True, facecolor='white', edgecolor='lightgray', loc='lower right')
sns.despine(ax=ax1)

if stat == "prop_and_sum":
    # plot the second plot (sum of the means) (this only works for the prop_and_sum statistic)
    for method, color in zip(["Uniform", "AT-LUCB", "BFTS"], ["blue", "green", "red"]):
        method_data = combined_df[combined_df['method'] == method]

        # adjust for AT-LUCB taking 2 samples per time step
        if method == "AT-LUCB":
            method_data = method_data.assign(actual_samples=method_data['samples'] * 2)
        else:
            method_data = method_data.assign(actual_samples=method_data['samples'])
        
        ax2.fill_between(
            method_data['actual_samples'], 
            method_data['sum_mu_lower'],
            method_data['sum_mu_upper'],
            color=color, 
            alpha=0.3
        )
        
        sns.lineplot(
            x='actual_samples', 
            y='sum_mu',
            data=method_data,
            color=color,
            linewidth=2,
            label=method,
            ax=ax2
        )

    # set the labels
    ax2.set_xlabel(r'$\#$ of samples', fontsize=14)
    ax2.set_ylabel(r'$\sum_{a\in J(t)}\mu_a$', fontsize=14)
    ax2.set_ylim(0, m)
    ax2.set_xlim(0, t)
    ax2.legend(fontsize=12, frameon=True, facecolor='white', edgecolor='lightgray', loc='lower right')
    sns.despine(ax=ax2)

# set a title
fig.suptitle(f"n={n}, m={m}, t={t}", fontsize=16)

# set tight layout
plt.tight_layout(pad=1.5, rect=[0, 0, 1, 0.95])

# save and plot the figure
plt.savefig(results_dir + '/' + experiment_name + '_combined.png', dpi=300)
plt.savefig('experiment_plots/' + experiment_name + '_combined.png', dpi=300)
plt.show()