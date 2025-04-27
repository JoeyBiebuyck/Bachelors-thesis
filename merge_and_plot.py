import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser


parser = ArgumentParser(description="XSS merge and plot")

parser.add_argument("-d", "--dir", dest="dir", type=str, required=True) # directory it will find the files in

args = parser.parse_args()

dir = args.dir

# merge the experiments

merged_atlucb_df = pd.read_csv(dir + "/atlucb-1.prop_of_success")
merged_atlucb_df.rename(columns={"prop_of_success": "prop_of_success_1"})

for i in range(2, 101):
    old_df = merged_atlucb_df
    new_filename = dir + "/atlucb-" + str(i) + ".prop_of_success"
    new_df = pd.read_csv(new_filename)
    merged_atlucb_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

merged_uniform_df = pd.read_csv(dir + "/uniform-1.prop_of_success")
merged_uniform_df.rename(columns={"prop_of_success": "prop_of_success_1"})

for i in range(2, 101):
    old_df = merged_uniform_df
    new_filename = dir + "/uniform-" + str(i) + ".prop_of_success"
    new_df = pd.read_csv(new_filename)
    merged_uniform_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

merged_atlucb_df.to_csv(dir + "/results/merged_atlucb_success_prop.csv", index=False)
merged_uniform_df.to_csv(dir + "/results/merged_uniform_success_prop.csv", index=False)

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

uniform_df = make_csv_plotable(results_dir + "/merged_uniform_success_prop.csv", "Uniform")
atlucb_df = make_csv_plotable(results_dir + "/merged_atlucb_success_prop.csv", "AT-LUCB")

combined_df = pd.concat([uniform_df, atlucb_df], ignore_index=True)

for method, color in zip(["Uniform", "AT-LUCB"], ["blue", "green"]):
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
plt.tight_layout()

plt.savefig(results_dir + '/first_plot.png')

# Show the plot
plt.show()