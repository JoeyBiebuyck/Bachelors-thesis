import pandas as pd

merged_atlucb_df = pd.read_csv("results/atlucb-1.prop_of_success")
merged_atlucb_df.rename(columns={"prop_of_success": "prop_of_success_1"})

for i in range(2, 101):
    old_df = merged_atlucb_df
    new_filename = "results/atlucb-" + str(i) + ".prop_of_success"
    new_df = pd.read_csv(new_filename)
    merged_atlucb_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

merged_uniform_df = pd.read_csv("results/uniform-1.prop_of_success")
merged_uniform_df.rename(columns={"prop_of_success": "prop_of_success_1"})

for i in range(2, 101):
    old_df = merged_uniform_df
    new_filename = "results/uniform-" + str(i) + ".prop_of_success"
    new_df = pd.read_csv(new_filename)
    merged_uniform_df = pd.merge(old_df, new_df, on="t", suffixes=("", f"_{i}"))

merged_uniform_df.to_csv("merged_uniform_success_prop.csv", index=False)